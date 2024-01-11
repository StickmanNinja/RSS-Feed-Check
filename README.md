# RSS-Feed-Check
A Flask Python application that displays RSS feeds for users with a master list that is automatically checked.
![Screenshot](https://raw.githubusercontent.com/StickmanNinja/RSS-Feed-Check/main/RSSExample.PNG)

In a real deployment, news feed results should be stored to MySQL database instead of to the "GlobalRSSList"
```
GlobalRSSList = list(set(SethRSSList + JackRSSList))
```
