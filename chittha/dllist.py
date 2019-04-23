# Chittha - a sticky notes application
# Copyright (C) 2019 Kunal Sinha <kunalsinha4u@gmail.com>
#
# Chittha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Chittha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Chittha.  If not, see <https://www.gnu.org/licenses/>.

class DLList:

    def __init__(self):
        self.head = None

    def add(self, node):
        if not self.head:
            self.head = node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            t = self.head
            while t.next != self.head:
                t = t.next
            t.next = node
            node.next = self.head
            node.prev = t
            self.head.prev = node

    def remove(self, node):
        if self.head:
            # only one element
            if node == self.head and self.head.next == self.head:
                self.head = None
            else:
                t = self.head
                count = 0
                while t != node:
                    if t == self.head:
                        count += 1
                        if count > 1:
                            print('Node not found')
                            break
                    t = t.next
                t.prev.next = t.next
                t.next.prev = t.prev
                if node == self.head:
                    self.head = t.next
        else:
            print('Node not found')

    # generator to return all the nodes in the list
    def all(self):
        if self.head:
            t = self.head
            count = 0 
            while True:
                if t == self.head:
                    count += 1
                    if count > 1:
                        break
                yield t
                t = t.next

    def length(self):
        if self.head:
            t = self.head.next
            length = 1
            while t != self.head:
                length += 1
                t = t.next
            return length
        else:
            return 0

