from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from collective.conference import _

class ISpeaker(form.Schema):
    """A conference speaker or leader of a workshop. Speaker can be added anywhere.
    """
    
    title = schema.TextLine(
            title=_(u"Name"),
        )
  
    street = schema.TextLine(
            title=_(u"Street"),
            required=False,
        )
    
    city = schema.TextLine(
            title=_(u"City"),
            required=False,
        )
    
    postalcode = schema.TextLine(
                 title=_(u"Postal Code"),
                 required=False,
        )
    
    country = schema.TextLine(
              title=_(u"Country"),
              required=False,
        )        

    email = schema.TextLine(
            title=_(u"E-Mail"),
            required=False,
        )

    telephonenummer = schema.TextLine(
            title=_(u"Telephone Number"),
            description=_(u"Please fill in your telephone number so that we could get in contact with you by phone if necessary."),
            required=False,
        )
    
    organisation = schema.TextLine(
            title=_(u"Organisation"),
            required=False,
        )

    description = schema.Text(
            title=_(u"A short bio"),
        )
    
    bio = RichText(
            title=_(u"Bio"),
            required=False
        )
    
    picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

@grok.subscribe(ISpeaker, IObjectAddedEvent)
def notifyUser(speaker, event):
    acl_users = getToolByName(speaker, 'acl_users')
    mail_host = getToolByName(speaker, 'MailHost')
    portal_url = getToolByName(speaker, 'portal_url')

    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    if not sender:
        return

    subject = "Is this you?"
    message = "A speaker /leader of a workshop called %s was added here %s" % (speaker.title, speaker.absolute_url(),)

    matching_users = acl_users.searchUsers(fullname=speaker.title)
    for user_info in matching_users:
        email = user_info.get('email', None)
        if email is not None:
            mail_host.secureSend(message, email, sender, subject)

class View(grok.View):
    grok.context(ISpeaker)
    grok.require('zope2.View')