# Facebook Comments Mining
A python script to mine all comments from a facebook page

## Usage
### Getting all comments from a Facebook Page
Run this command on your console to get all comments from a facebook page:
```
fb_comment_mining {fbpage}
```
where {fbpage} is your facebook page name (without the {}).

### Getting all comments from a Facebook Page that contain certain words:
```
fb_comment_mining {fbpage} {word} {word1} ...
```
where {fbpage} is your facebook page name (without the {}) and {word}, {word1} are the words you want to filter your comments. Only comments that contains {word} or {word1} are acquired.