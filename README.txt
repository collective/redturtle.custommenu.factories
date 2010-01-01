Summary
=======

This product make possible the customization of the Plone "*Add new...*" menu, commonly automatically
filled from the Plone available content types.

This is designed for avoiding useless content types but, at the same time, help UI experience of not
experienced users.

Of course, you can use this to add new non-standard stuff to the menu (like Javascript links).

Idea behind this
================

The case is related to developed content types arise only for *usability* enhancement of Plone sites.

One example: have you ever used Plone4ArtistsVideo, or collective.flowplayer?
In those products users that want to add new video to a site must use the "*Add new...*" menu and select
the *File* content.

So the editor (that is *never* a developer in real life... you must accept it) must know that when he add
a new file, it magically became a video... This is not so simple to understand; also is impossible to
understand it without a training or by past experience. Is not better to read "*Add new video*" instead?

So the best usability choice is to add a new content type to the menu. In many cases just copy/paste the
original used content if enough (in the example above, copy/paste the *File* content type and rename it
something like "Video").
But you know... we don't really need those new content types.

What users know about Plone?

* that for adding new content types, they must use the "*Add new...*"
* users often ignores the magic behind Plone (like the File that became a Video)
* developer don't like to add new silly content types only to help editors.

The problem above is related to the not-customizable state of the "Add new..." menu: the editor and the
developer will be both happy if a new, fake entry could be added to this menu.
Going back to the video example:

* the classic *File* entry (that point to *http://myhost/mysite/createObject?type_name=File*)
* a new "Video" entry (again pointing to *http://myhost/mysite/createObject?type_name=File*)

This products is designed only for this or similar usability issues.

How to use
==========

Installation
------------

Simply add the egg to your buildout, and re-run it.

::

    [instance]
    ...
    eggs =
        ...
        redturtle.custommenu.factories
    ...
    
    zcml =
        ...
        redturtle.custommenu.factories
        redturtle.custommenu.factories-overrides
    ...

After this, install the new product in Plone.

Uninstallation
--------------

You can *reinstall* the products safely without lose any customization data.
If you *uninstall* it, all customization will be removed from your Plone site, leaving no garbage
behind.

Customize the menu
------------------

In your "Add new..." menu you'll find a new "*Customize menu...*" entry. This will lead you to a
customization form where you can manage local menu changes of the current context.

The used *context* is always the *container* where you can find the context, or the context itself if it's
a container.

for every new entry you can/must fill this informations:

 `id`
     Enter here a string to be used to add an HTML id attribute to the new element. You can not provide
     it, but if you use an already existing ids, the new one will override the old.
     In this way you can *replace one of the native menu entry* with a new, customized ones.
 `name`
     Required.[BR]
     Provide the string to be used for displaying the new element.
 `description`
     The description is used to provide a tooltips hovering the element.
 `icon`
     A TALES expression that can be used to give an icon to the new element (very common).
 `condition`
     A TALES condition expression. If not provided, the new element is added to the menu. In provided
     it is evaluated as True or False, so the element is displayed or not.
 `URL`
     Required.[BR]
     A TALES expression used to render the HREF attribute on the link in the element. You have total freedom
     here: you can also render a string as "*javascript:...*" to provide some Javascript features.

TALES expressions
-----------------

In the TALES expression above, you can use those variables:

 `context`
     The current context, as Plone normal meaning
 `container`
     The container of the current context, or the context itself if the context is a container or you
     are viewing a *default document* in a folder.
 `portal_url`
     The *portal_url* tool, taken from the Plone site.

TODO
====

* localization
* browser tests
* javascript features for managing entries
* code needs refactoring
* make customization added to the site root available in every context, but make this inheritance optional
  and locally blockable.

