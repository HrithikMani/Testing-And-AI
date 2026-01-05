# Sample python test for webchart including MIE-Style comments
# Parsed comments available for viewing at: https://zeus.med-web.com/selenium/wc_test/

# Remember, using MIE-Style comments makes your test's intentions more understandable
# to people reading the TOC, it also means that if you plan out your outline of what
# and how to test, others can come in later and elaborate on your test.

# Also remember that plain old '#' style comments never get parsed, so feel free
# to liberally use terms like 'hack' and 'wtf' in these. These comments will be
# solely for other developers or yourself to read to document code, not design.

"""
# The following are our custom MIE-Style comments

#$ MIESection - Any comments and/or code following this comment gets grouped
                into a collapsible block in both the TOC and the results file.

                general bullet points in the flow of the test.

                    above general comments. These comments should include more
                    specific information, possibly specific data to be entered or used.

"""

# Your test MUST have a main function. It may have other functions, but it will always
# enter via the main function.
# * Note that MIE-Style comments are only parsed out of 'main' functions, so if you 
# * have helper functions, that is fine, but any documentation you put there will
# * not be recognized by the parser, nor will it appear in the selenium TOC

# Main parameters:
# d - an instance of MIEDriver. This is the object from which you will call
#       methods to control the browser.
# WCURL - A class defined in wcurls.py which contains common urls to be used
#         in conjunction with the navigate method. There are also some
#         browser definitions for you to branch your test based on which
#         browser is currently being used (d.browser == WCURL.BROWSER_CHROME)

def main(d, WCURL):
    """
    This is the docstring. Whatever you put here gets parsed as the highest
    level comment for your test. It is not collapsible, it is always visible.
    Put some thought into how you want to describe this ENTIRE test in this
    one description.
    """
    
    #$ Ensure the login page looks right before we even try to log in



    #$ Now test the login process



    # At this point the test is complete and this comment will not be parsed
    # There is no need for your main function to return anything
