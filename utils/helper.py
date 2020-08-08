import constants

from datetime import date
from xml.dom import minidom
from xml.etree.ElementTree import Comment, Element, ElementTree, tostring

def beautify_xml(xml_string):
    rough_string = tostring(xml_string, 'utf-8')

    return minidom.parseString(rough_string).toprettyxml()

def generate_xml(user_data, filename="Address_book"):
    top = Element('DeviceAddressBook_v5_2')
    top.append(Comment('Main Address Book'))

    address_book = []
    email_otk = []
    smb_otk = []

    for i in range(len(user_data)): 
        display_name = str(user_data[i][1]).title()
        email_address = str(user_data[i][3]).title()
        smb_path = str(user_data[i][4])
        #aonther_info = str(user_data[i][5])

        address_book.append(
            Element('Item', Type="Contact", Id=str(i+1), DisplayName= display_name, SendKeisyou="0", DisplayNameKana= display_name,\
                MailAddress=email_address, SendCorpName="", SendPostName="", SmbHostName=constants.SMB_HOSTNAME, SmbPath=smb_path,\
                SmbLoginPasswd=constants.SMB_LOGIN_PASSWD, SmbLoginName=constants.SMB_LOGIN_NAME, SmbPort=constants.SMB_PORT, FtpPath="", FtpHostName="", FtpLoginName="", FtpLoginPasswd="",\
                FtpPort="21", FaxNumber="", FaxSubaddress="", FaxPassword="", FaxCommSpeed="BPS_33600", FaxECM="On", FaxEncryptKeyNumber="0", FaxEncryption="Off",\
                FaxEncryptBoxEnabled="Off", FaxEncryptBoxID="0000", InetFAXAddr="", InetFAXMode="Simple", InetFAXResolution="3", InetFAXFileType="TIFF_MH",\
                IFaxSendModeType="IFAX", InetFAXDataSize="1", InetFAXPaperSize="1", InetFAXResolutionEnum="Default", InetFAXPaperSizeEnum="Default")
        )

        email_otk.append(
            Element('Item', Type="OneTouchKey", Id=str(i+1), DisplayName= display_name, AddressId=str(i+1), AddressType="EMAIL")
        )

        smb_otk.append(
            Element("Item", Type="OneTouchKey", Id=str(i + 1 + len(user_data)), DisplayName= display_name, AddressId=str(i+1), AddressType="SMB")
        )   

    top.extend(address_book)

    top.append(Comment('Email OneTouch Keys'))
    top.extend(email_otk)

    top.append(Comment('SMB OneTouch Keys'))
    top.extend(smb_otk)
    
    filename = filename + f" {date.today()}.xml"
    with open(filename, 'w') as f:
        f.write(beautify_xml(top))
    