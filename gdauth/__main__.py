#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2024, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2024. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

"""
Module containing an example on how to use GDAuth to access a Globus server, create 
directories and share them with users.

"""
import os
import sys
import pathlib
import argparse

from gdauth import log
from gdauth import config
from gdauth import globus
from gdauth import utils

def init(args):
    if not os.path.exists(str(args.config)):
        config.write(str(args.config))
    else:
        raise RuntimeError("{0} already exists".format(args.config))


def select(args):
    """
    Select collection/endpoint among the one sharedy by me       

    Parameters
    ----------
    args.app_uuid : Globus App / Client UUID
    args.ep_uuid  : Endpoint UUID
    """
    my_endpoints, endpoints_shared_with_me, endpoints_shared_by_me = globus.find_endpoints(args.app_uuid, args.ep_uuid)

    log.info('Show all endpoints shared and owned by my globus user credentials')

    log.info("*** Endpoints owned with me:")
    for key, value in my_endpoints.items():
        log.info("*** *** '{}' {}".format(key, value))

    log.info("*** Endpoints shared with me:")
    for key, value in endpoints_shared_with_me.items():
        log.info("*** *** '{}' {}".format(key, value))

    log.info("*** Endpoints shared by me:")
    for key, value in endpoints_shared_by_me.items():
        if value == args.ep_uuid:
            log.warning("Active: '{}' {}".format(key, value))
        else:
            log.info("*** *** '{}' {}".format(key, value))
        # endpoints[ep['display_name']] = ep['id']

    if utils.yes_or_no("Do you want to select a different collection ?"):

        for index, (key, value) in enumerate(endpoints_shared_by_me.items()):
            log.warning(f'{index}: {key}: {value}')

        log.error("Select a collection by entering its index")
        # Prompt the user to select an index
        user_input = input("Please select an index: ")

        # Validate and process the user input
        try:
            selected_index = int(user_input)
            if 0 <= selected_index < len(endpoints_shared_by_me):
                selected_key = list(endpoints_shared_by_me.keys())[selected_index]
                selected_value = endpoints_shared_by_me[selected_key]
                log.warning(f'You selected index {selected_index}: {selected_key}: {selected_value}')
                args.ep_uuid = selected_value
                # Update token file
                os.remove(os.path.join(str(pathlib.Path.home()), 'token.npy'))
                log.error("A new token will be generated next time you run GDAuth")
            else:
                log.warning("Invalid index. Please select a valid index.")
                log.warning("No collection/endpoint change. Endpoint is %s " % args.ep_uuid)
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        log.warning("No collection/endpoint change. Endpoint is %s " % args.ep_uuid)


def create(args):
    """
    Create a directory in a Globus endpoint    

    Parameters
    ----------
    args.dir      : Directory to be created in the share
    args.app_uuid : Globus App / Client UUID
    args.ep_uuid  : Endpoint UUID
    """
    # ep_uuid = globus.find_endpoint_uuid(args.app_uuid, args.ep_name)
    globus.create_dir(args.dir,       # Directory to be created in the share
                      args.app_uuid,  # Globus App / Client UUID
                      args.ep_uuid)   # Endpoint UUID

def share(args):
    """
    Create a directory in a Globus endpoint and share it with a user email address

    Parameters
    ----------
    args.dir      : Directory to be created in the share
    args.email    : User email address
    args.app_uuid : Globus App / Client UUID
    args.ep_uuid  : Endpoint UUID
    """
    globus.share(args.dir,      # Directory to be created in the share
                 args.email,    # User email address
                 args.app_uuid, # Globus App / Client UUID
                 args.ep_uuid   # Endpoint UUID
          )

def links(args):
    """
    Create the links for all items (folder and files) listed in the endpoint

    Parameters
    ----------
    args.dir      : Directory to be created in the share
    args.app_uuid : Globus App / Client UUID
    args.ep_uuid  : Endpoint UUID
    """

    # ep_uuid = globus.find_endpoint_uuid(args.app_uuid, args.ep_name)

    file_links, folder_links = globus.create_links(args.dir,       # Directory to be created in the share
                                                   args.app_uuid,  # Globus App / Client UUID
                                                   args.ep_uuid)   # Endpoint UUID

    for file_link in file_links:
        log.warning(file_link)
    for folder_link in folder_links:
        log.warning(folder_link)

def main():

    # This is just to print nice logger messages
    log.setup_custom_logger()

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])

    select_params   = config.SELECT_PARAMS
    create_params = config.CREATE_PARAMS
    share_params  = config.SHARE_PARAMS
    links_params  = config.LINKS_PARAMS

    cmd_parsers = [
        ('init',        init,           (),               "Create configuration file"),
        ('select',      select,         select_params,    "Select a Collection on the Globus server"),
        ('create',      create,         create_params,    "Create a folder in the Collection"),
        ('share',       share,          share_params,     "Share a Collection folder with a user email address"),
        ('links',       links,          links_params,     "Create download links for all items (folder and files) listed in a Collection folder"),
    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)

    try:
        # load args from default (config.py) if not changed
        args._func(args)
        config.log_values(args)
        # undate globus.config file
        sections = config.GDAUTH_PARAMS
        config.write(args.config, args=args, sections=sections)
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
