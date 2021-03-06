# Copyright (c) 2014, Juergen Riegel (FreeCAD@juergen-riegel.net)
# Copyright (c) 2011, Thomas Paviot (tpaviot@gmail.com)
# All rights reserved.

# This file is part of the StepClassLibrary (SCL).
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   Neither the name of the <ORGANIZATION> nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Simple Part21 STEP reader

Reads a given STEP file. Maps the enteties and instaciate the
corosbonding classes.
In addition it writes out a graphwiz file with the entity graph.
"""

import Part21,sys



__title__="Simple Part21 STEP reader"
__author__ = "Juergen Riegel, Thomas Paviot"
__url__ = "http://www.freecadweb.org"
__version__ = "0.1 (Jan 2014)"



class SimpleParser:
    """
    Loads all instances definition of a Part21 file into memory.
    Two dicts are created:
    self._instance_definition : stores attibutes, key is the instance integer id
    self._number_of_ancestors : stores the number of ancestors of entity id. This enables
    to define the order of instances creation.
    """
    def __init__(self, filename):
        import time
        import sys
        self._p21loader = Part21.Part21Parser("gasket1.p21")
        self.schemaModule = None
        self.schemaClasses = None

    def instaciate(self):
        """Instaciate the python classe from the enteties"""
        import inspect
        # load the needed schema module
        if self._p21loader.get_schema_name() == 'config_control_design':
            import config_control_design
            self.schemaModule = config_control_design
        if self._p21loader.get_schema_name() == 'automotive_design':
            import automotive_design
            self.schemaModule = automotive_design

        if self.schemaModule:
            self.schemaClasses = dict(inspect.getmembers(self.schemaModule))

        for number_of_ancestor in self._p21loader._number_of_ancestors.keys():
            for entity_definition_id in self._p21loader._number_of_ancestors[number_of_ancestor]:
                #print entity_definition_id,':',self._p21loader._instances_definition[entity_definition_id]
                self.create_entity_instance(entity_definition_id)

    def create_entity_instance(self, instance_id):
        instance_definition = self._p21loader._instances_definition[instance_id]
        print "Instance definition to process",instance_definition
        # first find class name
        class_name = instance_definition[0].lower()
        print "Class name:%s"%class_name

        if not class_name=='':
            object_ = self.schemaClasses[class_name]
            # then attributes
            print object_.__doc__
        #instance_attributes = instance_definition[1]
        #print "instance_attributes:",instance_attributes
        #a = object_(*instance_attributes)

if __name__ == "__main__":
    sys.path.append('..') # path where config_control_design.py is found
    parser = SimpleParser("gasket1.p21") # simple test file
    parser.instaciate()
