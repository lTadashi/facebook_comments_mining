import urllib.request
import json
import sys

def get_json(url):
	resposta = urllib.request.urlopen(url)
	json_string = resposta.read().decode('utf-8')
	json_obj = json.loads(json_string)
	return json_obj

if '--h' in sys.argv:
	print("\nUSE:\n\tfb_comment_mining facebook_page [tags]\n\n" + 
		"where\n\tfacebook_page\t\tName of the facebook page\n\n" +
		"\ttags\t\t\tSearching tags. The script search for the tags inside the comments\n\n" +
		"Options:\n\t--h\t\t... Shows this text\n\n" + 
		"Examples:\n\t> fb_comment_mining facebook_page\t\t... Search for all comments in all posts from facebook_page\n\n" +
		"\t> fb_comment_mining facebook_page foo\t\t... Search for all comments with the word foo in all posts from facebook_page\n\n" +
		"\t> fb_comment_mining facebook_page foo bar\t... Search for all comments with the word foo or bar in all posts from facebook_page");
	sys.exit()

# get page name
page = sys.argv[1]

tags = []
for num in range(2, len(sys.argv)):
	tags.append(sys.argv[num])

url_get_posts = "https://graph.facebook.com/v2.4/{p}/posts?access_token=1699611563644025|SU4myJqkKXubQgmfWBbl5BjBIaM&limit=100".format(p = page)
json_obj = get_json(url_get_posts)

# get all posts
print("\nGetting posts...");
posts = []
while 'paging' in json_obj:
	if 'next' in json_obj['paging']:
		for post in json_obj['data']:
			posts.append(post)
		json_obj = get_json(json_obj['paging']['next'])
num_posts = len(posts)		
print("Found " + str(num_posts) + " posts.\n")

url_get_comments = "https://graph.facebook.com/v2.5/$id/comments?access_token=1699611563644025|SU4myJqkKXubQgmfWBbl5BjBIaM&until=1342958811"
comments = []
cont = 1
for post in posts:
	post_id = post['id']
	url_get_comments = "https://graph.facebook.com/v2.5/{p}/comments?access_token=1699611563644025|SU4myJqkKXubQgmfWBbl5BjBIaM&until=1342958811".format(p = post_id)
	json_obj = get_json(url_get_comments)
	
	print("Getting comments from post " + str(cont) + " of " + str(num_posts) + "...", end = "\r")
	cont += 1

	for comment in json_obj['data']:
		if len(tags) > 0:
			for tag in tags:
				if tag.lower() in comment['message'].lower():
					comments.append(comment)
		else:
			comments.append(comment)
num_comments = len(comments)
if len(tags) > 0:
	print("\nFound " + str(num_comments) + " comments with the containing tags.\n")
else:
	print("\nFound " + str(num_comments) + " comments.\n")

# write the comments to the output file
print("Writing comments to the output file...")
mining_file_output = open('comments', 'wb')
for comment in comments:
	mining_file_output.write(('name: ' + comment['from']['name'] + '\n' + 'link: https://www.facebook.com/' + comment['from']['id'] + '\n' + 'message: ' + comment['message'] + '\n\n').encode('utf-8'));
mining_file_output.close()

print("Done.")