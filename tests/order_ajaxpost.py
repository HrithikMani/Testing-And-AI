try:
    from urllib import quote_plus as uriencode
except ImportError:
    from urllib.parse import quote_plus as uriencode
from xml.sax.saxutils import escape as xmlescape
from xml.dom import minidom
try:
    import StringIO
except ImportError:
    import io as StringIO


def dict_to_xml(o, tag_name):
    """Convert a dict object into XML text with
    values as attributes.

    """
    s = '<' + tag_name + ' '
    for k in o:
        s += k + '="' + xmlescape(o[k]) + '" '
    s += '/>'
    return s


def ajaxpost(d, order):
    """Post to the encoutnerorders ajaxpost function in webchart.
    Return parsed XML response.

    """
    xml = '<ORDERS>' + dict_to_xml(order, 'ENCORDER') + '</ORDERS>'
    querystring = 'f=ajaxpost&s=encounterorders&eorder_xml=' +  uriencode(xml)
    wccurl = d.getWCCurl(d._base_urls[-1])
    wccurl.setWCCookie('WCTESTSESSION')
    xml = wccurl.get('?' + querystring)
    if not xml:
        d.reportCommandStatus('ajaxpost', '', False, '', 'Server returned no response')
        return None
    try:
        dom = minidom.parse(StringIO.StringIO(xml))
    except Exception as e:
        d.reportCommandStatus('XML Parsing Failed', '', False, f'{e}', '')
        return
    return dom


def getElement(d, dom, tag_name):
    """Return the first named element from the DOM, reporting error
    if not found.

    """
    elements = dom.getElementsByTagName(tag_name)
    if len(elements) == 0:
        d.reportCommandStatus('res.getElementsByTagName', '', False, '', 'No ' + tag_name + ' elements found')
        return None
    d.reportCommandStatus('res.getElementsByTagName', '', True, '', tag_name + ' element found')
    return elements[0]


def main(d, WCURL):
    """ Orders AJAXPOST testing

    """
    d.startSection('Insert order')
    order = {
        "pat_id": "18",
        "order_id": "1234",
        "order_name": "Test"
    }
    res = ajaxpost(d, order)
    added = getElement(d, res, 'ENCORDER')
    d.endSection()
    if not added:
        return

    d.startSection('Update order')
    enc_order_id = added.getAttribute('enc_order_id')
    order['enc_order_id'] = enc_order_id
    order['comments'] = 'Tomorrow, at sunrise, I shall no longer be here.'
    res = ajaxpost(d, order)
    updated = getElement(d, res, 'ENCORDER')
    if not updated:
        return
    if updated.getAttribute('comments') != order['comments']:
        d.reportCommandStatus('updated.getAttribute', '', False, '', 'Comment not updated properly')
        return
    d.reportCommandStatus('updated.getAttribute', '', True, '', 'Comment update successful')
    d.endSection()

