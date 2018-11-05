import web

urls = (
    '/', 'Index',
    '/search', 'Search'
)
render = web.template.render('templates/', base='base')

search_box = web.form.Form(web.form.Textbox('q', web.form.notnull))


class Index:
    def GET(self):
        # f = login()
        # return render.formtest(f)
        return render.index(search_box())


class Search:
    def GET(self):
        search_box_copy = search_box()
        if search_box_copy.validates():
            return render.search(search_box_copy['q'].value)
        else:
            raise web.notfound()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
