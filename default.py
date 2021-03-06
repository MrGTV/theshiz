 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil
from resources.modules import client,control,tools,shortlinks
from datetime import date
import xml.etree.ElementTree as ElementTree
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.shiztv'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

accounticon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'account.png'))
livetvicon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'livetv.png'))
catchupicon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'catchup.png'))
vodicon	     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'vod.png')) 
seriesicon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'tv.png'))
settingsicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'settings.png'))
logouticon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'logout.png'))
searchicon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'search.png'))
currenticon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'current.png'))
allowedicon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'allowed.png'))
usericon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'user.png'))
passicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'pass.png'))
cacheicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'clear.png'))
advancedicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'eas.png'))
speedicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'speed.png'))
dataicon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'meta.png'))
xxxicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'xxx.png'))
dateicon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'date.png'))
statusicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'status.png'))

username     = control.setting('Username')
password     = control.setting('Password')

host         = 'http://s1.vbhosting.xyz'
port         = '1337'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
panel_api	 = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
all_series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series&cat_id=0'%(host,port,username,password)

Guide = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.shiztv/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.shiztv/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))
#########################################


def start():
	if username=="":
		user = userpopup()
		passw= passpopup()
		control.setSetting('Username',user)
		control.setSetting('Password',passw)
		xbmc.executebuiltin('Container.Refresh')
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		if auth == "":
			line1 = "Login Details Incorrect"
			line2 = "Please Try Again" 
			line3 = "" 
			xbmcgui.Dialog().ok('Attention', line1, line2, line3)
			start()
		else:
			line1 = "Login Successful"
			line2 = "Welcome to Shiz TV!" 
			line3 = ('[COLOR skyblue]%s[/COLOR]'%user)
			xbmcgui.Dialog().ok('Shiz TV', line1, line2, line3)
			addonsettings('ADS2','')
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		if not auth=="":
			tools.addDir('[B][COLOR white]Account Details[/COLOR][/B]','url',6,accounticon,fanart,'')
			tools.addDir('[B][COLOR white]Live Channels[/COLOR][/B]','live',1,livetvicon,fanart,'')
			tools.addDir('[B][COLOR white]Movies[/COLOR][/B]','url',11,vodicon,fanart,'')
			tools.addDir('[B][COLOR white]TV Shows[/COLOR][/B]','url',12,seriesicon,fanart,'')
			tools.addDir('[B][COLOR white]Tools[/COLOR][/B]','url',16,settingsicon,fanart,'')
			tools.addDir('[B][COLOR white]Log Out[/COLOR][/B]','LO',10,logouticon,fanart,'')
            
def home():
	tools.addDir('Account Details','url',6,icon,fanart,'')
	tools.addDir('Live Channels','live',1,icon,fanart,'')
	tools.addDir('Movies','url',11,icon,fanart,'')
	tools.addDir('TV Shows','url',12,icon,fanart,'')
	tools.addDir('Tools','url',16,icon,fanart,'')
	tools.addDir('Log Out','LO',10,icon,fanart,'')

def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			tools.addDir('%s'%name,url1,2,icon,fanart,'')
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					tools.addDir('%s'%name,url1,2,icon,fanart,'')

def livelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))

def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				if xbmcaddon.Addon().getSetting('hidexxx')=='true':
					tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
				else:
					if not 'XXX' in name:
						if not 'Adult' in name:
							tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)	
		
####################################################################################
def search_scat(url):
    text = searchdialog()
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR green][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    return scat(url,text)

def scat(url,search=None):
    #log(url)
    open = tools.OPEN_URL(url)
    #log(open)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            name = base64.b64decode(name)
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            #log((search,name))
            if search == None or (search.lower() in name.lower()):
                tools.addDir(str(name).replace('?',''),url1,24,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def seasons(url):
    if url =="seasons":
        open = tools.OPEN_URL(seasons_url)
    else:
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,21,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def eps(url):
    open = tools.OPEN_URL(url)
    #print open
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,22,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################
def series(url):
    log(url)
    if url =="vod":
        open = tools.OPEN_URL(vod_url)
    else:
        open = tools.OPEN_URL(url)
    log(open)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,20,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
		
#####################################################################

def stream_video(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def subm():
	tools.addDir('[COLOR white]All Movies[/COLOR]','vod',333,vodicon,fanart,'')
	tools.addDir('[COLOR white]Movie Categories[/COLOR]','vod',3,vodicon,fanart,'')
	tools.addDir('[COLOR white]Search Movies[/COLOR]','url',5,searchicon,fanart,'')

def subt():
	tools.addDir('[COLOR white]TV Show Categories[/COLOR]',series_url,24,seriesicon,fanart,'')
	tools.addDir('[COLOR white]Search TV Shows[/COLOR]',all_series_url,2424,searchicon,fanart,'')

def searchdialog():
	search = control.inputDialog(heading='Search Shiz TV:')
	if search=="":
		return
	else:
		return search

	
def search():
    if mode==([3, 4, 20, 21]):
        return False
    #text = searchdialog()
    text = xbmcgui.Dialog().input("Search for a Movie ?")
    xbmc.log(repr(text),xbmc.LOGERROR)
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR skyblue][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    import json
    j = json.loads(open)
    available_channels = j["available_channels"]
    for id,channel in available_channels.items():
        name = channel["name"] or ''
        type = channel["stream_type"] or ''
        ext = channel["container_extension"] or ''
        thumb = channel["stream_icon"] or ''
        fanart = ''
        liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
        xbmc.log(repr(name))
        if text in name.lower():
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
        elif text not in name.lower() and text in name:
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	
def addonsettings(url,description):
	if   url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok('Shiz TV', 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Shiz TV', 'Set Advanced Settings')
	elif url =="tv":
		dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup', ['iVue TV Guide','PVR TV Guide','Both'])
		if dialog==0:
			ivueint()
			xbmcgui.Dialog().ok('Shiz TV', 'iVue Integration Complete')
		elif dialog==1:
			pvrsetup()
			xbmcgui.Dialog().ok('Shiz TV', 'PVR Integration Complete')
		elif dialog==2:
			pvrsetup()
			ivueint()
			xbmcgui.Dialog().ok('Shiz TV', 'PVR & iVue Integration Complete')
	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.shiztv/resources/modules/speedtest.py")')
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="XXX":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('hidexxx','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	
def all_movies():
	open = tools.OPEN_URL(panel_api)
	import json
	j = json.loads(open)
	available_channels = j["available_channels"]
	for id,channel in available_channels.items():
		name = channel["name"] or ''
		type = channel["stream_type"] or ''
		ext = channel["container_extension"] or ''
		thumb = channel["stream_icon"] or ''
		fanart = ''
		liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
		liz.setProperty('fanart_image', fanart)
		liz.setProperty("IsPlayable","true")
		play_url	 = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
def asettings():
	choice = xbmcgui.Dialog().yesno('Shiz TV', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	open = tools.OPEN_URL(panel_api)
	try:
		username   = tools.regex_from_to(open,'"username":"','"')
		password   = tools.regex_from_to(open,'"password":"','"')
		status     = tools.regex_from_to(open,'"status":"','"')
		connects   = tools.regex_from_to(open,'"max_connections":"','"')
		active     = tools.regex_from_to(open,'"active_cons":"','"')
		expiry     = tools.regex_from_to(open,'"exp_date":"','"')
		expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
		expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month     = tools.MonthNumToName(month)
			year      = re.sub(' -.*?$','',year)
			expiry    = month+' '+day+' - '+year
			tools.addDir('[B][COLOR skyblue]Account Status :[/COLOR][/B] %s'%status,'','',statusicon,fanart,'')
			tools.addDir('[B][COLOR skyblue]Expiry Date:[/COLOR][/B] '+expiry,'','',dateicon,fanart,'')
			tools.addDir('[B][COLOR skyblue]Username :[/COLOR][/B] '+username,'','',usericon,fanart,'')
			tools.addDir('[B][COLOR skyblue]Password :[/COLOR][/B] '+password,'','',passicon,fanart,'')
			tools.addDir('[B][COLOR skyblue]Allowed Connections:[/COLOR][/B] '+connects,'','',allowedicon,fanart,'')
			tools.addDir('[B][COLOR skyblue]Current Connections:[/COLOR][/B] '+ active,'','',currenticon,fanart,'')
	except:pass
		
	
def extras():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		XXX = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		XXX = '[B][COLOR red]OFF[/COLOR][/B]'
	tools.addDir('Metadata is %s'%META,'META',10,dataicon,fanart,META)
	tools.addDir('XXX Channels are %s'%XXX,'XXX',10,xxxicon,fanart,XXX)
	tools.addDir('Clear Cache','CC',10,cacheicon,fanart,'')
	tools.addDir('Edit Advanced Settings','ADS',10,advancedicon,fanart,'')
	tools.addDir('Run a Speed Test','ST',10,speedicon,fanart,'')
    
params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)

elif mode==2:
	livelist(url)

elif mode==3:
	vod(url)
    
elif mode==333:
	all_movies()
    
elif mode==4:
	stream_video(url)

elif mode==5:
	search()

elif mode==6:
	accountinfo()

elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')

elif mode==10:
	addonsettings(url,description)
    
elif mode==11:
	subm()

elif mode==12:
	subt()

elif mode==13:
	catchup()

elif mode==14:
	tvarchive(name,description)
	
elif mode==15:
	listcatchup2()
	
elif mode==16:
	extras()

elif mode==17:
	shortlinks.Get()

elif mode==19:
	get()

elif mode==20:
	series(url)

elif mode==21:
	seasons(url)

elif mode==22:
	eps(url)

elif mode==24:
	scat(url)

elif mode==2424:
    search_scat(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
