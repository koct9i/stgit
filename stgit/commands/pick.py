__copyright__ = """
Copyright (C) 2005, Catalin Marinas <catalin.marinas@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""

import sys, os
from optparse import OptionParser, make_option

from stgit.commands.common import *
from stgit.utils import *
from stgit import stack, git


help = 'import a patch from a different branch or a commit object'
usage = """%prog [options] [<patch@branch>|<commit>]

Import a patch from a different branch or a commit object into the
current series. By default, the name of the imported patch is used as
the name of the current patch. It can be overriden with the '--name'
option. A commit object can be reverted with the '--reverse'
option. The log and author information are those of the commit object."""

options = [make_option('-n', '--name',
                       help = 'use NAME as the patch name'),
           make_option('-r', '--reverse',
                       help = 'reverse the commit object before importing',
                       action = 'store_true')]


def func(parser, options, args):
    """Import a commit object as a new patch
    """
    if len(args) != 1:
        parser.error('incorrect number of arguments')

    check_local_changes()
    check_conflicts()
    check_head_top_equal()

    commit_str = args[0]
    patch_branch = commit_str.split('@')

    if len(patch_branch) == 2:
        patch = patch_branch[0]
    elif options.name:
        patch = options.name
    else:
        raise CmdException, 'Unkown patch name'

    commit_id = git_id(commit_str)
    commit = git.Commit(commit_id)

    if not options.reverse:
        bottom = commit.get_parent()
        top = commit_id
    else:
        bottom = commit_id
        top = commit.get_parent()

    message = commit.get_log()
    author_name, author_email, author_date = \
                 name_email_date(commit.get_author())

    print 'Importing commit %s...' % commit_id,
    sys.stdout.flush()

    crt_series.new_patch(patch, message = message, can_edit = False,
                         unapplied = True, bottom = bottom, top = top,
                         author_name = author_name,
                         author_email = author_email,
                         author_date = author_date)
    crt_series.push_patch(patch)

    print 'done'
    print_crt_patch()