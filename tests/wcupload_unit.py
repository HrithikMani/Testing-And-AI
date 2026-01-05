"""
    Unit Test for wcUpload js control 
    @owners: sgrider
    @filedeps: jsbin/wcupload.js
"""
import json

from wcunittest import wcElement, wcJSCode

LAYOUT_MODULE = 'wcupload_unit'
LAYOUT_NAME = 'wcupload_unit_control'

CONTROL_NAME = 'wcuploadControl'

# these are the default options that get can be overridden when writing out the layout template
DEFAULT_OPTS = {
    'label': None,
    'id': None,
    'vars': None,
    'accept': None,
    'headers': None,
    'userdata': None,
    'debug': None,
    'maxWidth': None,
    'multiFile': None,
    'checkboxes': None,
    'firstControlColumn': None,
    'postColumns': None,
    'postColumnsExclude': None,
    'showSectionTotal': None,
    'showSectionChecked': None,
    'defaultChecked': None,
    'showJumpLinks': None,
    'showBatchControls': None,
    'notifyDuplicateFile': None,
    'notifyInvalidFile': None,
    'notifyInvalidColumn': None,
    'maxFiles': None,
    'maxBytes': None,
    'displayCB': None,
    'uploadCB': None,
    'responseCB': None,
    'previewTypes': None,
    'previewSize': None,
    'lightweight': None,
    'scrollable': None,
    'varCollisions': None,
    'ignoreEmptyCollisions': None,
    'typeCB': None,
    'skipDefaultTypeCheck': None,
    'allowDuplicates': None,
    'duplicateCB': None,
    'skipDefaultDuplicateCheck': None,
    'multiSection': None,
    'indexFields': None,
    'indexKeys': None,
    'indexKeysStrict': None,
    'indexCB': None
}
# This is the default control layout template
CONTROL_TEMPLATE = """
<WCINCLUDE module="FileUpload" name="css" />
<WCSCRIPT src="wcupload.js" />
<div id="container" />
<script>
window.onload = function() {{
    window.{} = wcupload('container', {{
        label: {label},
        id: {id},
        vars: {vars},
        accept: {accept},
        headers: {headers},
        userdata: {userdata},
        debug: {debug},
        maxWidth: {maxWidth},
        multiFile: {multiFile},
        checkboxes: {checkboxes},
        firstControlColumn: {firstControlColumn},
        postColumns: {postColumns},
        postColumnsExclude: {postColumnsExclude},
        showSectionTotal: {showSectionTotal},
        showSectionChecked: {showSectionChecked},
        defaultChecked: {defaultChecked},
        showJumpLinks: {showJumpLinks},
        showBatchControls: {showBatchControls},
        notifyDuplicateFile: {notifyDuplicateFile},
        notifyInvalidFile: {notifyInvalidFile},
        notifyInvalidColumn: {notifyInvalidColumn},
        maxFiles: {maxFiles},
        maxBytes: {maxBytes},
        displayCB: {displayCB},
        uploadCB: {uploadCB},
        responseCB: {responseCB},
        previewTypes: {previewTypes},
        previewSize: {previewSize},
        lightweight: {lightweight},
        scrollable: {scrollable},
        varCollisions: {varCollisions},
        ignoreEmptyCollisions: {ignoreEmptyCollisions},
        typeCB: {typeCB},
        skipDefaultTypeCheck: {skipDefaultTypeCheck},
        allowDuplicates: {allowDuplicates},
        duplicateCB: {duplicateCB},
        skipDefaultDuplicateCheck: {skipDefaultDuplicateCheck},
        multiSection: {multiSection},
        indexFields: {indexFields},
        indexKeys: {indexKeys},
        indexKeysStrict: {indexKeysStrict},
        indexCB: {indexCB}
    }});
}};
</script>
"""

def insertControl(d, c):
    opts = DEFAULT_OPTS.copy()
    opts.update(c)
    # Now turn each option value in the options to a valid js identifier
    for k, v in opts.items():
        opts[k] = json.dumps(v)
    d.miedb.dbExec("REPLACE INTO layout (module, name, active, layout_html) VALUES "\
        "(%s, %s, 1, %s)", LAYOUT_MODULE, LAYOUT_NAME,
        CONTROL_TEMPLATE.format(CONTROL_NAME, **opts))

def clearList(d):
    d.clickElement(value='Clear List')

def uploadFile(d, filename):
    # In order to be able to interact with this file uploader, the actual
    # <input type="file"> needs to be visible, so we'll unhide it, and then rehide it
    d.runJS("document.getElementsByName('file_control')[0].style.display = ''")
    d.enterFormData(filename, name='file_control')
    d.runJS("document.getElementsByName('file_control')[0].value = ''")
    d.runJS("document.getElementsByName('file_control')[0].style.display = 'none'")

def gotoLayout(d):
    d.navigate('?f=layout&module={}&name={}'.format(LAYOUT_MODULE, LAYOUT_NAME))

def main(d, WCURL):
    u = d.getWCUnitTest('Verify default presentation')
    u.setup(insertControl, {
        'label': 'File',
    }, reason='Just use the defaults')
    u.verifyElements([
        wcElement('value', 'Choose Files', disabled=None),
        wcElement('value', 'Upload File', disabled=True),
        wcElement('value', 'Clear List', disabled=True),
        wcElement('xpath', "//span[text()='Drop files here']")
    ], reason='Check for basic UI elements')
    u.test(gotoLayout, reason='Load the page')

    u = d.getWCUnitTest('Drop a single file and verify defaults')
    u.setup(insertControl, {
        'label': 'File',
    }, reason='Just use the defaults')
    u.setup(gotoLayout, reason='Load the page')
    u.setup(uploadFile, 'wcupload.csv')
    u.verifyElements([
        wcElement('value', 'Choose Files', disabled=None),
        wcElement('value', 'Upload File', disabled=None),
        wcElement('value', 'Clear List', disabled=None),
        wcElement('xpath', "//span[text()='Drop files here']"),
        wcElement('xpath', "//input[@type='checkbox']", checked=False, disabled=None),
        wcElement('xpath', "//span[@title='Remove File']"),
    ], reason='Check for basic UI elements')
    u.verifyElements([
        wcElement('xpath', "//th[text()='filename']"),
        wcElement('xpath', "//th[text()='size']"),
    ], reason='Check for default headers')
    u.verifyJS(wcJSCode('{}.getRows().length'.format(CONTROL_NAME), 1),
        reason='There should only be 1 row')
    u.test()

    u = d.getWCUnitTest('Drop two identical files')
    u.setup(insertControl, {
        'label': 'File',
    }, reason='Just use the defaults')
    u.setup(gotoLayout, reason='Load the page')
    u.setup(uploadFile, 'wcupload.csv')
    u.setup(uploadFile, 'wcupload.csv')
    u.verifyJS(wcJSCode('wcnotify.getWarnings().length', 1), reason='Look for a warning')
    u.verifyJS(wcJSCode('{}.getRows().length'.format(CONTROL_NAME), 1),
        reason='There should only be 1 row due to default dup checking')
    u.verifyElements([
        wcElement('value', 'Choose Files', disabled=None),
        wcElement('value', 'Upload File', disabled=None),
        wcElement('value', 'Clear List', disabled=None),
        wcElement('xpath', "//span[text()='Drop files here']"),
        wcElement('xpath', "//input[@type='checkbox']", checked=False, disabled=None),
        wcElement('xpath', "//span[@title='Remove File']"),
    ], reason='Check for basic UI elements')
    u.verifyElements([
        wcElement('xpath', "//th[text()='filename']"),
        wcElement('xpath', "//th[text()='size']"),
    ], reason='Check for default headers')
    u.test()

    u = d.getWCUnitTest('Verify clear button works')
    u.setup(insertControl, {
        'label': 'File',
    }, reason='Just use the defaults')
    u.setup(gotoLayout, reason='Load the page')
    u.setup(uploadFile, 'wcupload.csv')
    u.verifyElements([
        wcElement('value', 'Choose Files', disabled=None),
        wcElement('value', 'Upload File', disabled=True),
        wcElement('value', 'Clear List', disabled=True),
        wcElement('xpath', "//span[text()='Drop files here']"),
        wcElement('xpath', "//input[@type='checkbox']", exists=False),
    ], reason='Check for basic UI elements')
    u.verifyElements([
        wcElement('xpath', "//th[text()='filename']", exists=False),
        wcElement('xpath', "//th[text()='size']", exists=False),
    ], reason='Check for default headers')
    u.verifyJS(wcJSCode('{}.getRows().length'.format(CONTROL_NAME), 0),
        reason='There should be no rows')
    u.test(clearList, reason='Click the clear button')


