Summary
=======

This product make possible the customization of the Plone "*Add new...*" menu, commonly automatically
filled from the Plone available content types.

This is designed for avoiding useless content types but, at the same time, help UI experience of simple
users.

Of course, you can use this to add new non-standard stuff to the menu (like Javascript links).

Idea behind this
================

In my experience, many developed content types rise only for *usability* enhancement of Plone sites.

One of the best (worst?) example is Plone4ArtistsVideo product: users that want to add new video to a site
must use the "*Add new...*" menu and select the *File* content.

So the editor (that is *never* a developer in real life... we must accept it) must know that when he add
a new file, it magically became a video...

The best usability choice is to add a new content type to the menu. In many cases just copy/paste the
original used content if enough (in the example above, copy/paste the *File* content type and rename it
something like "Video").
But you know... we don't really need those new content types.

* users knows that for add new content types to Plone sites, they must use the "*Add new...*"
* users often ignores the magic behind Plone (like the File that became a Video)
* developer don't like to add new silly content types only to help editors.

Another example: knows that the "File" must be used both for a PDF document and an executable...

The problem here is only that the "add contents menu" is not customizable: the editor and the developer
will be both happy if a new, fake entry could be added to this menu.
Going back to the video example:

* the classic *File* entry (that point to *http://myhost/mysite/createObject?type_name=File*)
* a new "Video" entry (again pointing to *http://myhost/mysite/createObject?type_name=File*)

