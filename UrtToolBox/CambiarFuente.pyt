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
        self.canRunInBackground = True
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

        wksDescribe = arcpy.Describe(viejaFuente)
        tipoFuente = wksDescribe.workspaceType

        mxd = arcpy.mapping.MapDocument("CURRENT")
        layers = arcpy.mapping.ListLayers(mxd)

        for layer in layers :
          try : 
            arcpy.AddMessage("Nombre Dataset: {}".format(layer.datasetName)) 
            arcpy.AddMessage("Fuente Datos: {}".format(layer.dataSource))
            if(tipoFuente == 'RemoteDatabase') :
              server = wksDescribe.connectionProperties.server
              instance = wksDescribe.connectionProperties.instance
              database = wksDescribe.connectionProperties.database
              version = wksDescribe.connectionProperties.version

              arcpy.AddMessage("Servidor {}".format(server))
              arcpy.AddMessage("Instancia {}".format(instance))
              arcpy.AddMessage("Base de Datos {}".format(database))
              arcpy.AddMessage("Version {}".format(version))

              change = server in layer.dataSource or viejaFuente in layer.dataSource
            else :
              change = str(viejaFuente) in layer.dataSource


            if(change) :
              arcpy.AddMessage("Cambiar")
              layer.replaceDataSource(nuevaFuente, "NONE", layer.datasetName)
              arcpy.AddMessage(layer.dataSource)
          except Exception as ex :
            arcpy.AddMessage(ex.message)
            arcpy.AddMessage(ex.args)
        
        mxd.save()
        return
