


import dropbox

client = dropbox.client.DropboxClient('fecjcnqs73dhim4')
print ('linked account: ', client.account_info())

f = open('working-draft.txt', 'rb')
response = client.put_file('/magnum-opus.txt', f)
print('uploaded: ', response)

folder_metadata = client.metadata('/')
print('metadata: ', folder_metadata)

f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
out = open('magnum-opus.txt', 'wb')
out.write(f.read())
out.close()
print (metadata)