#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  msgpackencode.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
import msgpack


class MSGPackDecode(Actor):

    '''**Decodes MSGPack data into Python objects.**

    Decodes the payload or complete events from MSGPack format.

    Parameters:

        - source(str)('@data')
           |  The location of the msgpack data to decode.

        - destination(str)('@data')
           |  The location to store the decoded data.

    Queues:

        - inbox
           |  Incoming messages

        - outbox
           |  Outgoing messges
    '''

    def __init__(self, actor_config, complete=False, source='@data', destination='@data'):
        Actor.__init__(self, actor_config)

        self.pool.createQueue("inbox")
        self.pool.createQueue("outbox")
        self.registerConsumer(self.consume, "inbox")

    def consume(self, event):

        event.set(msgpack.unpackb(event.get(self.kwargs.source)), self.kwargs.destination)
        self.submit(event, self.pool.queue.outbox)
