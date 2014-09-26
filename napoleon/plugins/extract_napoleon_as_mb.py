import os

import pyblish.api
import napoleon.plugin

from maya import cmds


@pyblish.api.log
class NapoleonExtractAsMb(napoleon.plugin.Extractor):
    """Extract family members of a napoleon.model as Maya ASCII"""

    families = ['napoleon.model', 'napoleon.rig.animation']
    hosts = ['maya']
    version = (0, 1, 0)
    optional = False
    name = 'Extract Model as Maya Binary'

    def process_instance(self, instance):
        """Returns list of value and exception"""
        self.log.info("Extracting mb..".format(instance))
        previous_selection = cmds.ls(selection=True)

        cmds.select(instance,
                    replace=True,
                    noExpand=True)  # Make sure sets are preserved

        name = instance.data('name')
        name = pyblish.api.format_filename(name)

        with self.temp_dir() as temp_dir:
            temp_file = os.path.join(temp_dir, name + ".mb")
            cmds.file(temp_file,
                      type='mayaBinary',
                      exportSelected=True,
                      preserveReferences=False)

            self.commit(path=temp_dir, instance=instance)

        if previous_selection:
            cmds.select(previous_selection,
                        replace=True,
                        noExpand=True)
        else:
            cmds.select(deselect=True,
                        noExpand=True)

        self.log.info("Extraction successful.")
