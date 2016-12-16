# -*- coding: utf-8 -*-
# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
'''
文件说明：该python脚本根据传入的元素去寻找依赖元素，最终返回依赖元素结合
    分别从依赖元素下的 element-provides 和 element-deps 获取其它依赖元素
    需要注意的是，用户若自定义依赖元素，则总的依赖目录是以冒号分隔的字符串 -- 但是代码中只处理一层循环，若有客户自定义，则默认的元素路径则废弃
'''
from __future__ import print_function
import argparse
import collections
import logging
import os
import sys

import diskimage_builder.logging_config

logger = logging.getLogger(__name__)

# 从环境变量中获取元素的目录--这是传递共享参数的一种方式
# 在common-defaults中设置了默认值为 elements目录
def get_elements_dir():
    if not os.environ.get('ELEMENTS_PATH'):
        raise Exception("$ELEMENTS_PATH must be set.")
    return os.environ['ELEMENTS_PATH']

# 从元素目录中取出指定元素集合，默认返回空集
def _get_set(element, fname, elements_dir=None):
    if elements_dir is None:
        elements_dir = get_elements_dir()
    # 如果客户自己定义了元素路径，则与默认元素路径以冒号分隔
    for path in elements_dir.split(':'):
        # 这里将path, element, fname拼接为一个路径
        element_deps_path = (os.path.join(path, element, fname))
        try:
            with open(element_deps_path) as element_deps:
                # 这里是否有问题？第一次循环就返回了，后面的怎么办？--------------------------------- bug ？？
                # 个人认为：用户要自己指定元素路径，则的包含所有的元素（包括系统定义的）--- 这里可否优化：只指定用户定义的，需要的系统依赖，同样到系统目录中寻找
                return set([line.strip() for line in element_deps])
        except IOError as e:
            # errno.errorcode.keys() 列举errno错误代码，此处errno.ENOENT 为 2 表示没有该文件或目录
            if os.path.exists(os.path.join(path, element)) and e.errno == 2:
                return set()
            if e.errno == 2:
                continue
            else:
                raise

    logger.error("Element '%s' not found in '%s'" % (element, elements_dir))
    sys.exit(-1)


# 获取指定的元素集合（element-providers）-- 大多数这里取出来的是 'operating-system'
def provides(element, elements_dir=None):
    """Return the set of elements provided by the specified element.

    :param element: name of a single element
    :param elements_dir: the elements dir to read from. If not supplied,
                         inferred by calling get_elements_dir().

    :return: a set just containing all elements that the specified element
             provides.
    """
    return _get_set(element, 'element-provides', elements_dir)

# 从指定的元素路径下获取 element-deps这个文件中的内容，组成一个集合返回
def dependencies(element, elements_dir=None):
    """Return the non-transitive set of dependencies for a single element.

    :param element: name of a single element
    :param elements_dir: the elements dir to read from. If not supplied,
                         inferred by calling get_elements_dir().

    :return: a set just containing all elements that the specified element
             depends on.
    """
    return _get_set(element, 'element-deps', elements_dir)


def expand_dependencies(user_elements, elements_dir=None):
    """Expand user requested elements using element-deps files.

    Arguments:
    :param user_elements: iterable enumerating the elements a user requested
    :param elements_dir: the elements dir to read from. Passed directly to
                         dependencies()

    :return: a set containing user_elements and all dependent elements
             including any transitive dependencies.
    """
    # 将传递的数组转换为集合 -- 假如为['base', 'centos7', 'vm']
    final_elements = set(user_elements)
    check_queue = collections.deque(user_elements)
    provided = set()
    provided_by = collections.defaultdict(list)
    # 这里将依赖元素和元素提供者找出来
    while check_queue:
        # bug #1303911 - run through the provided elements first to avoid
        # adding unwanted dependencies and looking for virtual elements
        # 从队列开头取出一个元素
        element = check_queue.popleft()
        # 避免获取重复的元素
        if element in provided:
            continue
        # 单独将依赖（element-deps）和提供者（element-provides）的集合获取
        element_deps = dependencies(element, elements_dir)
        element_provides = provides(element, elements_dir)
        # save which elements provide another element for potential
        # error message
        # 遍历元素提供者，然后组织数据结构，字典，以提供者为键，值为元素列表，即，一个提供者，都有哪些元素需要
        for provide in element_provides:
            provided_by[provide].append(element)
        provided.update(element_provides)
        # 过滤掉已经存在的元素
        check_queue.extend(element_deps - (final_elements | provided))
        final_elements.update(element_deps)

    if "operating-system" not in provided:
        logger.error(
            "Please include an operating system element.")
        sys.exit(-1)
    # 用户元素中不能多填，比如provided已经提供了，则不再写
    conflicts = set(user_elements) & provided
    if conflicts:
        logger.error(
            "The following elements are already provided by another element")
        for element in conflicts:
            logger.error("%s : already provided by %s" %
                         (element, provided_by[element]))
        sys.exit(-1)
    return final_elements - provided


def main(argv):
    # 首先加载logging配置
    diskimage_builder.logging_config.setup()

    parser = argparse.ArgumentParser()
    # 使用nargs='+' 或者 '*' 表示传入待解析的参数必须为一个列表，'*' 表示至少0个，'+'表示至少1个
    parser.add_argument('elements', nargs='+',
                        help='display dependencies of the given elements')
    parser.add_argument('--expand-dependencies', '-d', action='store_true',
                        default=False,
                        help=('(DEPRECATED) print expanded dependencies '
                              'of all args'))

    args = parser.parse_args(argv[1:])

    if args.expand_dependencies:
        logger.warning("expand-dependencies flag is deprecated,  "
                       "and is now on by default.", file=sys.stderr)
    # 将结果转换为字符串输出
    print(' '.join(expand_dependencies(args.elements)))
    return 0
