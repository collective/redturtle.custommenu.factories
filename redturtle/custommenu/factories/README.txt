Introduction a basical use
==========================

Welcome to the guide of the usage of redturtle.custommenu.factories.
We need to setup something before this file can became a real and working browser test for Plone.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Ok, now we are ready to load the Plone site where this product is installed.

    >>> browser.open(portal_url)

Our first test is to see that the "Customize menu..." element of the factories menu can't be used
from normal users.

    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = 'secret'
    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

So the link to access the customization can't be in the current page. A Contributor can add a new content
type (like a "News Item") but can't see the new command.

    >>> browser.getLink('News Item').text
    '[IMG] News Item'
    >>> "Customize menu\xe2\x80\xa6" in browser.contents
    False

Again, the contributor user can't go directly to the customization form if he know the URL.

    >>> browser.open(portal_url+"/@@customize-factoriesmenu")
    >>> "You do not have sufficient privileges to view this page" in browser.contents
    True

Only Manager (or role that behave the "*Customize menu: factories*" permission) can access the
customization feature.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> "You are now logged in" in browser.contents
    True

Now the "Customize menu" link must the there.

    >>> "Customize menu\xe2\x80\xa6" in browser.contents
    True
    >>> browser.getLink('Customize menu\xe2\x80\xa6').click()

Now test if we are arrived in a form needed to explicitly enable customization per-context.

    >>> "Factories menu management activation" in browser.contents
    True

Before beeing able to add or customize menu elements, we need to activate the feature here, in the site
root.

    >>> browser.getControl(name='enable-command').click()

Now we are again the the customization form, but the form is changed. We can test to be at the same URL,
but now with a nice activation message.

    >>> browser.url == portal_url+'/@@customize-factoriesmenu'
    True
    >>> 'Enabled local customizations' in browser.contents    
    True

From this new form we can of course disable the customization. Be aware that this will also delete all
customizations added to the context.

    >>> browser.getControl(name='disable-command').click()
    >>> browser.url == portal_url
    True
    >>> 'Local customizations disabled' in browser.contents    
    True

Ok, so now we're going back to the customization form, enable it for the site root and going over.

    >>> browser.open(portal_url+'/@@customize-factoriesmenu')
    >>> browser.getControl(name='enable-command').click()

The customization view now is empty (no customization are there).

Adding a new element
--------------------

The simplest thing we can do is to add an alias for another existing content type. As ofter the "File"
entity can be unfriendly (not all users see a PDF file as a File), we can create a new entry named
"PDF Document".

The idea is to keep inner Plone feature to handle PDF files (so still we will use the File content type)
but we change the UI for final users.

Let's fill the form.

    >>> browser.getControl(name='element-id').value = 'pdf-file'
    >>> browser.getControl(name='element-name').value = 'PDF Document'
    >>> browser.getControl(name='element-descr').value = 'A file content to be filled with a PDF document'
    >>> browser.getControl(name='icon-tales').value = 'string:$portal_url/pdf_icon.gif'
    >>> browser.getControl(name='element-tales').value = 'string:${container/absolute_url}/createObject?type_name=File'

We skipped the optional *condition-tales* that can be used to control when the customized entry must
appear in the UI.

Now we can submit the form and see the result.

    >>> browser.getControl(name='add-command').click()
	>>> 'New entry added' in browser.contents
	True

First of all we are still in the customization form.

    >>> browser.url == portal_url+'/@@customize-factoriesmenu'
    True

The entry we just added is now available for be updated or deleted, in another form of the same view.

    >>> browser.getControl(name='element-name:list').value
    'PDF Document'

Now it's time to test what new feature we added to the site. Going back to the site root we can now rely
on our new entry in the factories menu.

    >>> browser.open(portal_url)
    >>> browser.getLink('PDF Document').text
    '[IMG] PDF Document'

Also, all other given attributes has been used.

    >>> browser.getLink('PDF Document').attrs['title']
    'A file content to be filled with a PDF document'
    >>> browser.getLink('PDF Document').attrs['id']
    'pdf-file'
    
But for the user, the real interesting thing is the "new" content type. Click on the new link in the menu
will lead us to add a normal Plone File content.

    >>> browser.getLink('PDF Document').click()
    >>> 'An external file uploaded to the site.' in browser.contents
    True

When adding new element, some entry data (name and TALES expression for the URL) are required. We are forced
to provide both of them.

    >>> browser.open(portal_url+'/@@customize-factoriesmenu')
    >>> browser.getControl(name='element-id').value = 'fake'
    >>> browser.getControl(name='element-descr').value = 'fake'
    >>> browser.getControl(name='icon-tales').value = 'fake'
    >>> browser.getControl(name='add-command').click()
    >>> 'Please, provide all required data' in browser.contents
    True
    >>> browser.getControl(name='element-id').value = 'fake'
    >>> browser.getControl(name='element-name').value = 'fake'
    >>> browser.getControl(name='element-descr').value = 'fake'
    >>> browser.getControl(name='icon-tales').value = 'fake'
    >>> browser.getControl(name='add-command').click()
    >>> 'Please, provide all required data' in browser.contents
    True
    >>> browser.getControl(name='element-id').value = 'fake'
    >>> browser.getControl(name='element-descr').value = 'fake'
    >>> browser.getControl(name='icon-tales').value = 'fake'
    >>> browser.getControl(name='element-tales').value = 'fake'
    >>> browser.getControl(name='add-command').click()
    >>> 'Please, provide all required data' in browser.contents
    True
    >>> browser.getControl(name='element-id').value = 'fake'
    >>> browser.getControl(name='element-name').value = 'fake'
    >>> browser.getControl(name='element-descr').value = 'fake'
    >>> browser.getControl(name='icon-tales').value = 'fake'
    >>> browser.getControl(name='element-tales').value = 'fake'
    >>> browser.getControl(name='add-command').click()
    >>> 'Please, provide all required data' in browser.contents
    False
    >>> 'New entry added' in browser.contents
    True

In the last example above we added a completely non-sense new element. But The menu customization feature
heavily on the TALES expression for the URL. In the given data can't be transformed in a valid TALES
expression, the whole entry is ignored.

So, going back to the site root we don't see any "*fake*" link available, even if the "*PDF Document*"
ones is still there.

    >>> browser.open(portal_url)
    >>> 'fake' in browser.contents
    False
    >>> 'PDF Document' in browser.contents
    True

Removing entries
----------------

Just for keep things clean, but obviously also for giving to users a way to remove added customization,
the form provided has the feature to removed stored entries.

First of all, be sure that our "*fake*" element is in the form.

    >>> browser.open(portal_url+'/@@customize-factoriesmenu')
    >>> browser.getControl(name='element-name:list', index=1).value
    'fake'

Also the first (and good) entry is there.

    >>> browser.open(portal_url+'/@@customize-factoriesmenu')
    >>> browser.getControl(name='element-name:list', index=0).value
    'PDF Document'

To delete one or more entries we must use the "*Delete selected*" button. First we must select one or
more entries. Click on the button without select an entry will return an error to the user, and no
real action will be performed.

    >>> browser.getControl(name='delete-command').click()
    >>> 'Please, select at least one entry to be deleted' in browser.contents
    True
    >>> browser.url == portal_url+'/@@customize-factoriesmenu'
    True

Ok, now we remove the garbage of the "*fake*" element.

    >>> browser.getControl('Delete?', index=1).click()
    >>> browser.getControl(name='delete-command').click()
    >>> 'Customization/s remove' in browser.contents
    True

Now we don't see anymore the "*fake*" entry in the form.

    >>> 'fake' not in browser.contents
    True


Modify and update existing entries
----------------------------------

The next and last "simple" task is to modify existing entry for local menu customization.
In the next example we keep al the data for our "*PDF Document*" but we wanna change the mandatory
description.

    >>> browser.getControl('Element description', index=0).value
    'A file content to be filled with a PDF document'
    >>> browser.getControl('Element description',
    ...                    index=0).value = 'A PDF document (ok, this is again a File content)'

We must now click on the "*Save changes*" button.

    >>> browser.getControl('Save changes').click()
    >>> 'Customization/s updated' in browser.contents
    True
    >>> browser.getControl('Element description', index=0).value
    'A PDF document (ok, this is again a File content)'

We are still in the form, so we can continue to change again our entry. Like for adding new ones, required
data must be provided.

    >>> browser.getControl('Element name', index=0).value = ''
    >>> browser.getControl('Save changes').click()
    >>> 'Please, provide all required data' in browser.contents
    True

To make a real test of the changes, let's go back to the site root and see if the link title has been
changed.

    >>> browser.open(portal_url)
    >>> browser.getLink('PDF Document').attrs['title']
    'A PDF document (ok, this is again a File content)'


Advanced use
============

The customization can give us more power and new features thanks to::

 `Condition for entry`
     We can provide a condition TALES expression that will be evaluated to make an element appear or not
 `Multiple contexts`
     We can customize different entries in different context all around the site. As seen before the site
     root is a context, but a very special ones.
 `Inheritance`
     The "*Inherit*" check will give us the power to enable/disable acquisition of customization defined
     in the site root to lower contexts.
 `Override and obfuscate`
     Using the *id* we can override inherit customization but also original menu elements.
     We can also hide elements using a *False* condition.

Before going on with examples, let's prepare a new context to work on. We now create a new Folder content
inside our Plone site.

    >>> browser.getLink('Folder').click()
    >>> browser.getControl('Title').value = 'New area'
    >>> browser.getControl('Description').value = 'Welcome to a new area of the site'
    >>> browser.getControl('Save').click()

Next, we go again to the customization form.

    >>> browser.getLink('Customize menu\xe2\x80\xa6').click()
    >>> browser.url == portal_url+'/new-area/@@customize-factoriesmenu'
    True

Use TALES conditions
--------------------

Let's introduce power of condition with an example. Let's say that in our "*New area*" we want to handle
a special kind on Event content type. But this event must be addable to our new area if and only if a
special marker keyword is used on the area itself.

xxx