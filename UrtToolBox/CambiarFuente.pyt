import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "UrtToolBox"
        self.alias = "Toolbox URT - Migracion ArcGIS Server"

        # List of tool classes associated with this toolbox
        self.tools = [ReemplazarFuente]
        
class ReemplazarFuente(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Reemplazar Fuente Capas"
        self.description = "Reemplazar Fuente Capas"
        self.canRunInBackground = False
        self.Params = {'viejaFuente': 0, 'nuevaFuente': 1}

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []

        param0 = arcpy.Parameter(displayName = "Antiguo Espacio de Trabajo", 
          name='viejaFuente', 
          datatype='DEWorkspace', 
          parameterType='Required', 
          direction='Input')
        params.insert(self.Params['viejaFuente'], param0)

        param1 = arcpy.Parameter(displayName = "Nuevo Espacio de Trabajo", 
          name='nuevaFuente', 
          datatype='DEWorkspace', 
          parameterType='Required', 
          direction='Input')
        params.insert(self.Params['nuevaFuente'], param1)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        nuevaFuente = parameters[self.Params['nuevaFuente']].value
        viejaFuente = parameters[self.Params['viejaFuente']].value

        arcpy.AddMessage(nuevaFuente)
        arcpy.AddMessage(viejaFuente)

        mxd = arcpy.mapping.MapDocument("CURRENT")
        mxd.findAndReplaceWorkspacePaths(viejaFuente, nuevaFuente)
        mxd.save()

        return 
