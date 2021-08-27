# Created by Ruslan Huseynov
import arcpy
import pythonaddins
import wx
import wx.adv
import sys
import os

locator = os.path.expanduser('~') + '\Documents\ArcGIS\Default.gdb'


class AtributTransfer(object):

    dlg = None
   
    def __init__(self):
        self.enabled = True
        self.checked = False
        
    def onClick(self):
 
         
        if self.dlg is None:
            self.dlg = TRANSFER1()
            
            
        else:
            self.dlg.Show(True)
            
        return


class TRANSFER1(wx.Frame):

    

    def __init__(self):


         wxStyle = wx.CAPTION | wx.RESIZE_BORDER | wx.MINIMIZE_BOX |wx.CLOSE_BOX | wx.SYSTEM_MENU

         wx.Frame.__init__(self, None, -1, "Atribut Transfer", style=wxStyle, size=(900, 650))

         self.SetMaxSize((900, 650))

         self.SetMinSize((900, 650))

         self.Bind(wx.EVT_CLOSE, self.OnClose)
    


         panel = wx.Panel(self, -1)

         panel.SetBackgroundColour("#939393")

         self.Centre()

         font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)

         font1 = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)

         


         ########################## Labeller ################################
         ####################################################################

         wx.StaticText(panel, -1, "Əsas data :", pos=(7,16)).SetFont(font)

         wx.StaticText(panel, -1, "Hədəf :", pos=(17,66)).SetFont(font)

         wx.StaticText(panel, -1, "Fields :", pos=(440,63)).SetFont(font)

         wx.StaticText(panel, -1, "Fields :", pos=(440,17)).SetFont(font)

         ####################################################################
         ####################################################################


         ########################## STATIC_BOX  ##########################################################
         #################################################################################################

         self.box = wx.StaticBox(panel, -1, "Seçim " ,pos=(104,415),size=(180,80)).SetFont(font)

         self.box1 = wx.StaticBox(panel, -1, "Seçim metodu " ,pos=(290,415),size=(275,80)).SetFont(font)

         self.box2 = wx.StaticBox(panel, -1, "Yazdirma metodu " ,pos=(570,415),size=(255,80)).SetFont(font)

         self.box3 = wx.StaticBox(panel, -1, "Axtarış radiusu " ,pos=(570,500),size=(255,70)).SetFont(font)

         ###############################################################################################################
         ###############################################################################################################



         ########################## COMBOBOX  ##########################################################
         #################################################################################################

         edc=[]  # esas data choice geden melumatlar

         hc = []  # hedef dataya geden melumatlar

         edfc = []  # esas datanin field goruntusu

         hf = []  # hedef datasini field siyahisi

         esas_data_layer_melumatlari = []
         esas_data_field_melumatlari = []
         hedef_data_layer_melumatlari = []
         hedef_data_field_melumatlari = []
         

         self.esas_data_combo = wx.Choice(panel ,choices = edc, pos = (106,11),size=(320,50))

         self.esas_data_field_combo=wx.Choice(panel,choices = edfc , pos = (506,11),size=(320,50))

         self.hedef_combo = wx.Choice(panel ,choices =hc , pos = (106,60),size=(320,50))

         self.hedef_field_combo=wx.Choice(panel,choices = hf , pos = (506,60),size=(320,50))

         self.secim_metodu_selection=wx.ComboBox(panel, value ="INTERSECT",  choices =["INTERSECT","INTERSECT_3D","WITHIN_A_DISTANCE_GEODESIC",
                 "WITHIN_A_DISTANCE","WITHIN_A_DISTANCE_3D","CONTAINS",
                 "COMPLETELY_CONTAINS","CONTAINS_CLEMENTINI","WITHIN",
                 "COMPLETELY_WITHIN","WITHIN_CLEMENTINI","ARE_IDENTICAL_TO",
                 "BOUNDARY_TOUCHES","SHARE_A_LINE_SEGMENT_WITH",
                 "CROSSED_BY_THE_OUTLINE_OF","HAVE_THEIR_CENTER_IN",
                 "CLOSEST_GEODESIC","CLOSEST"]  , pos = (300,445),size=(255,30))

         
         

         self.yazdirma_metodu_selection=wx.ComboBox(panel ,value = "JOIN_ONE_TO_ONE", choices =["JOIN_ONE_TO_ONE","JOIN_ONE_TO_MANY"] , pos = (580,445),size=(235,30))

         

         self.metrik_deyerler=wx.ComboBox(panel,value ="Meters",  choices = ["Unknown","Centimeters","Decimal degrees",
                    "Decimeters","Feet","Inches","Kilometers",
                    "Meters","Miles","Millimeters","Nautical Miles",
                    "Points","Yards"], pos = (635,530),size=(180,30))

         

         self.Hedef_list = wx.ListBox(panel, size = (723,230), choices = [], style = wx.LB_SINGLE,pos=(104,155))

         self.Hedef_list.SetBackgroundColour("white")

         self.Hedef_list.SetFont(font1)

         

         ###############################################################################################################
         ###############################################################################################################


         ########################## BUTTONLAR  ##########################################################

 


         self.hedefe_elave_et_button = wx.Button(panel, label="HƏDƏFLƏRƏ ƏLAVƏ ET", pos=(104,110),size=(723,40),id = 15)

         self.hedefe_elave_et_button.SetBackgroundColour("#367272")

         self.hedefe_elave_et_button.SetFont(font)



         self.Yazdir_Button = wx.Button(panel, label="YAZDIR", pos=(103,510),size=(450,60),id=5)

         self.Yazdir_Button.SetBackgroundColour("#367272")

         self.Yazdir_Button.SetFont(font)




         self.Temizle = wx.Button(panel, label="Təmizlə", pos=(670,390),size=(157,23),id=44)

         self.Temizle.SetBackgroundColour("#367272")

         self.Temizle.SetFont(font)

         

         

         

         self.Melumat = wx.Button(panel, label="Məlumat", pos=(7,575),size=(80,25),id=1)

         self.Melumat.SetBackgroundColour("#367272")

         self.Melumat.SetFont(font)
         
    


         

         self.Bind(wx.EVT_BUTTON, self.Melumatlarim,id=1)  # Melumat goruntuleme
         
         

         self.esas_data_combo.Bind(wx.EVT_CHOICE, self.ESAS)  # Esas datanin field goruntusu
         


         self.hedef_combo.Bind(wx.EVT_CHOICE , self.HEDEF)   # Hedef datanin field goruntusu

         

         self.Bind(wx.EVT_BUTTON , self.ListeGonder,id=15)  # Listeye melumat gonderme

         self.Bind(wx.EVT_BUTTON , self.ListTemizle,id=44)

         self.Bind(wx.EVT_BUTTON , self.SpatialJoin,id=5)


         ########################## Radio buttonlar ############################################################################

         self.Secim_et_radio = wx.RadioButton(panel,22, label = 'Seçimi istifadə et',size=(160,30 ),pos = (120,435)).SetFont(font)

         self.Secimi_legv_radio = wx.RadioButton(panel,22, label = 'Seçimi ləğv et',size=(160,30 ),pos = (120,460)).SetFont(font)

         ###############################################################################################################
         ###############################################################################################################

         ########################## TextCntrl(Entry) ############################################################################

         self.mesafe_gir = wx.TextCtrl(panel, -1, value="0", pos=(580,530),size=(45,28))

         ##########################################################################################################################

         self.Show(True)



    
    def OnClose(self, event):

        self.Show(False)
        
        self.esas_data_combo.Clear()
        
        self.esas_data_field_combo.Clear()
        
        self.hedef_combo.Clear()

        self.hedef_field_combo.Clear()
        
        self.Hedef_list.Clear()

        

        mxd = arcpy.mapping.MapDocument("CURRENT")

        for lyr in arcpy.mapping.ListLayers(mxd):
            
            self.esas_data_combo.Append(lyr.name)

            self.hedef_combo.Append(lyr.name)


   

    

    def Melumatlarim(self, event):

        licence = """Arcgis üzərinə yazılmış olan və Arcgislə birgə çalışan
Geometry_Attribute_Transfer tamamilə  pulsuz bir uzantıdır.
Hər kəs tərəfindən rahatlıqla istifadə edilə bilər.
İstifadə qaydası çox rahatdır.
Heç bir atribut məlumatı uyğun olmadığı
təqdirdə yerləşmə mövqeyinə əsasən(geometry)
eyni anda birdən çox atribut məlumatını
digər datanın atribut məlumatlarına yazdırmaq üçün yaradılmışdır...
"""


        info = wx.adv.AboutDialogInfo()

        
        info.SetName('Geometry Attribute Transfer')
        info.SetVersion('2021')
        info.SetCopyright('(C) 2021 ITMIM')
        #info.SetWebSite('http://www.github.com/Ruslan281')
        info.SetLicence(licence)
        info.AddDeveloper('''Developer : Hüseynov Ruslan
Consulting : Vüsal Rüstəmov
Gmail : huseynov.ruslan555@gmail.com
Tel : +994 55-281-96-78
GitHub : http://www.github.com/Ruslan281
''')
       

        wx.adv.AboutBox(info)




#############Backend##################################

        
######################  Esas datanin field funksiyasi  #######################################################
    def ESAS(self,event):

        fields = arcpy.ListFields(self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()))

        for field in fields:

            self.esas_data_field_combo.Append(field.name)


            
#######################################################################################################
#######################################################################################################
            


######################  Hedef datanin field funksiyasi  #######################################################
    def HEDEF(self,event):

        fields = arcpy.ListFields(self.hedef_combo.GetString(self.hedef_combo.GetSelection()))

        for field in fields:

            self.hedef_field_combo.Append(field.name)

            
#######################################################################################################
#######################################################################################################
        

        
    def ListeGonder(self,event):

        if self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()) == '' and self.hedef_combo.GetString(self.hedef_combo.GetSelection()) == '':

                                         wx.MessageBox("Xahiş olunur 'Əsas data' və  'Hədəf data' seçin", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)

        elif self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()) == '':

            wx.MessageBox("Əsas data  boş ola bilməz !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif self.hedef_combo.GetString(self.hedef_combo.GetSelection()) == '':

            wx.MessageBox("Hədəf data boş ola bilməz !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)



        elif self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()) == '' and self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()) == '':

            wx.MessageBox("'Əsas data' və 'Hədəf data' field məlumatları boş ola bilməz !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()) == '':

            wx.MessageBox("'Əsas data' field məlumatları boş ola bilməz !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()) == '':

            wx.MessageBox("'Hədəf data' field məlumatları boş ola bilməz !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        

        else:

            self.Hedef_list.Append("{}({})  ===>  {}({})".format(self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()),
                                                           self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()),
                                                           self.hedef_combo.GetString(self.hedef_combo.GetSelection()),
                                                           self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection())))


            esas_data_layer_melumatlari.append(self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()))

            esas_data_field_melumatlari.append(self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()))

            hedef_data_layer_melumatlari.append(self.hedef_combo.GetString(self.hedef_combo.GetSelection()))

            hedef_data_field_melumatlari.append(self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()))

            




    def ListTemizle(self,event):

        self.Hedef_list.Clear()
        
        esas_data_layer_melumatlari.clear()
        
        esas_data_field_melumatlari.clear()
        
        hedef_data_layer_melumatlari.clear()
        
        hedef_data_field_melumatlari.clear()


                        
    def SpatialJoin(self,event):

        b= "{} {}".format(self.mesafe_gir.GetValue(),self.metrik_deyerler.GetValue())
                  

        if self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()) == '':
             
                                         wx.MessageBox("Xahiş olunur 'Əsas data' və 'Hədəf data' - nın bütün sütunlarını doldurun !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)

        elif self.hedef_combo.GetString(self.hedef_combo.GetSelection()) == '':

            wx.MessageBox("Xahiş olunur 'Əsas data' və 'Hədəf data' - nın bütün sütunlarını doldurun !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()) == '':

            wx.MessageBox("Xahiş olunur 'Əsas data' və 'Hədəf data' - nın bütün sütunlarını doldurun !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()) == '':

            wx.MessageBox("Xahiş olunur 'Əsas data' və 'Hədəf data' - nın bütün sütunlarını doldurun !", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


        elif  self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()) == self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()):

            cal1= '[{}_1]'.format(self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()))
            

            arcpy.SpatialJoin_analysis(self.hedef_combo.GetString(self.hedef_combo.GetSelection()), self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()),
                                   locator + '\Joins',
                                   self.yazdirma_metodu_selection.GetValue(),
                                   'KEEP_ALL', '#',
                                   self.secim_metodu_selection.GetValue(),
                                   b, '#')

            arcpy.CalculateField_management(locator + '\Joins',
                                        self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()),
                                        cal1, 'VB', '#')

            arcpy.DeleteRows_management(self.hedef_combo.GetString(self.hedef_combo.GetSelection()))

            arcpy.Append_management(locator + '\Joins',
                                self.hedef_combo.GetString(self.hedef_combo.GetSelection()), 'NO_TEST')


            arcpy.Delete_management('Joins', '#')

            arcpy.Delete_management(locator + '\Joins', '#')


            wx.MessageBox("Məlumat uğurla yazıldı..", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


            self.Show(False)

        
            self.Hedef_list.Clear()


            


            

        else:

            cal = '[{}]'.format(self.esas_data_field_combo.GetString(self.esas_data_field_combo.GetSelection()))


            arcpy.SpatialJoin_analysis(self.hedef_combo.GetString(self.hedef_combo.GetSelection()), self.esas_data_combo.GetString(self.esas_data_combo.GetSelection()),
                                   locator + '\Joins',
                                   self.yazdirma_metodu_selection.GetValue(),
                                   'KEEP_ALL', '#',
                                   self.secim_metodu_selection.GetValue(),
                                   b, '#')

            

            arcpy.CalculateField_management(locator + '\Joins',
                                        self.hedef_field_combo.GetString(self.hedef_field_combo.GetSelection()),
                                        cal, 'VB', '#')


            arcpy.DeleteRows_management(self.hedef_combo.GetString(self.hedef_combo.GetSelection()))


            arcpy.Append_management(locator + '\Joins',
                                self.hedef_combo.GetString(self.hedef_combo.GetSelection()), 'NO_TEST')


            arcpy.Delete_management('Joins', '#')


            arcpy.Delete_management(locator + '\Joins', '#')


            wx.MessageBox("Məlumat uğurla yazıldı..", 'Məlumat',
                                                       wx.OK | wx.ICON_INFORMATION)


            self.Show(False)
 
            self.Hedef_list.Clear()

            

       
App = wx.PySimpleApp()
App.MainLoop()



