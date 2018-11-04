import formshare.resources as r
import os


def create_resources(apppath, config):
    r.add_library('formshare', os.path.join(apppath, 'jsandcss'), config)

    # ----------------------------Basic CSS-----------------------
    r.add_css_resource('formshare', 'bootstrap', 'css/bootstrap.min.css')
    r.add_css_resource('formshare', 'font-5', 'font-awesome/css/all.css')
    r.add_css_resource('formshare', 'font-awesome', 'font-awesome/css/v4-shims.css')
    r.add_css_resource('formshare', 'sweetalert', 'css/plugins/sweetalert/sweetalert.css')
    r.add_css_resource('formshare', 'animate', 'css/animate.css')
    r.add_css_resource('formshare', 'style', 'css/style.css')
    r.add_css_resource('formshare', 'rtl', 'css/plugins/bootstrap-rtl/bootstrap-rtl.min.css', 'bootstrap')

    # ----------------------------Basic JS----------------------------------------------------
    r.add_js_resource('formshare', 'jquery', 'js/jquery-3.1.1.min.js')
    r.add_js_resource('formshare', 'popper', 'js/popper.min.js')
    r.add_js_resource('formshare', 'bootstrap', 'js/bootstrap.min.js')
    r.add_js_resource('formshare', 'metismenu', 'js/plugins/metisMenu/jquery.metisMenu.js')
    r.add_js_resource('formshare', 'slimscroll', 'js/plugins/slimscroll/jquery.slimscroll.min.js')
    r.add_js_resource('formshare', 'pace', 'js/plugins/pace/pace.min.js')
    r.add_js_resource('formshare', 'wow', 'js/plugins/wow/wow.min.js')
    r.add_js_resource('formshare', 'sweetalert', 'js/plugins/sweetalert/sweetalert.min.js', 'pace')
    r.add_js_resource('formshare', 'inspinia', 'js/inspinia.js', None)

    # ----------------------------Profile----------------------------------
    r.add_css_resource('formshare', 'bsmarkdown', 'css/plugins/bootstrap-markdown/bootstrap-markdown.min.css',
                       'sweetalert')
    r.add_js_resource('formshare', 'bsmarkdown', 'js/plugins/bootstrap-markdown/bootstrap-markdown.js', None)
    r.add_js_resource('formshare', 'markdown', 'js/plugins/bootstrap-markdown/markdown.js', 'bsmarkdown')
    r.add_js_resource('formshare', 'clipboard', 'js/plugins/clipboard/clipboard.js', None)

    # ------------------------------Add/Edit project--------------------------------------
    r.add_css_resource('formshare', 'switchery', 'css/plugins/switchery/switchery.css', None)
    r.add_js_resource('formshare', 'switchery', 'js/plugins/switchery/switchery.js', None)
