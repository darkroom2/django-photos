Design and implement a simple backend application for managing photos.

We want to store photo title, album ID, width, height and dominant color (as a hex code) in local database; the files
should be stored in local filesystem.

Functionalities:

* Photos REST resource (list, create, update, delete):
    * Output fields (list): ID, title, album ID, width, height, color (dominant color), URL (URL to locally stored file)
    * Input fields (create, update): title, album ID, URL


* Import photos from external API at https://jsonplaceholder.typicode.com/photos:
    * via REST API
    * via CLI script


* Import photos from JSON file (expecting the same data format as the external API's):
    * via REST API
    * via CLI script

Suggestions:

* Use any frameworks and libraries you'll find useful for the task (we prefer Django)
* Try to follow the best coding practices
* Don't be afraid to write tests
