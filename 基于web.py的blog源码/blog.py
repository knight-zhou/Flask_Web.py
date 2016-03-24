#coding:utf8
import web
import model
import os

### Url mappings
#第一部分是匹配URL的正则表达式，像/、/help/faq、/item/(\d+)等(\d+将匹配数字)。
urls = (
    '/', 'Index',                        #这行表示我们要URL/(首页)被一个叫index的类处理。
    '/help','Help',                       #定义用一个help的url，由Help类去处理
    '/abc','Abc',                       #定义用一个help的url，由Help类去处理
    '/view/(\d+)', 'View',                   #匹配/view/后面加数字，并由View类去处理
    '/new', 'New',                                    #如果new的url路由到New类实现，http://127.0.0.1:8080/new
    # '/hello','Hello'
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)  #这会告诉web.py到你的模板目录中去查找模板。


class Index:

    def GET(self):                   #当有人用GET请求/时，这个GET函数随时会被web.py调用
        """ Show page """
        posts = model.get_posts()
        return render.index(posts)


# #定义Help类
# class Help:
#     def GET(self):
#         raise web.seeother('/static/help.html')    #跳转到static下的help页面
#         # return "This is help page!"            #返回页面信息

#定义Help类
class Help:
    def GET(self):
        name='tttt'
        return render.knight(name)          #渲染到knight.html的模板页面

class Abc:
    def GET(self):
        name='tttttttttt'
        city='shenzhen '                   #尝试传两个值
        cwd=os.getcwd()                  #定义当前目录
        return render.abc(name,city,cwd)          #渲染到knight.html的模板页面,传入三个参数



class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)

#定义提交类
class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,             #定义了一个表单Textbox
            size=40,
            description="提交的主题:"),
        web.form.Textarea('content', web.form.notnull,            #定义了一个表单Textarea
            rows=30, cols=80,
            description="提交的内容:"),
        web.form.Button('Post entry'),                           #定义了一个button
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)                          #渲染到new的html页面,渲染form
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


app = web.application(urls, globals())             #现在我们需要创建一个列举这些url的application。

if __name__ == '__main__':
    app.run()