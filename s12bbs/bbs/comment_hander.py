#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
# Author:Zhou Ming

def add_node(tree_dic,comment):
    if comment.parent_comment is None:
        #如果我的父评论为None,代表我是顶层
        tree_dic[comment] = {}

    else: # 循环当前整个字典,直到找到为止
        for k,v in tree_dic.items():
            if k == comment.parent_comment: #找到了父级评论
                print("find dad.",k)
                tree_dic[k][comment] = {}
            else: #进入下一层继续找
                print("keep going deeper ...")
                add_node(v,comment)


def build_tree(comment_set):
    # print(comment_set)
    tree_dic = {}
    for comment in comment_set:
        add_node(tree_dic,comment)

    print('--------------------')
    for k,v in tree_dic.items():
        print(k,v)
    return tree_dic

def render_tree_node(tree_dic,margin_val):
    html = ""
    for k,v in tree_dic.items():
        ele = "<div class = 'comment-node' style='margin-left:%spx' comment-id=%s> "%(margin_val,k.id) + k.comment + "<span style='margin-left:10px'>%s</span>"%k.date \
              + "<span style='margin-left:10px'>%s</span>"%k.user.name  \
              + '<span class="glyphicon glyphicon-comment  add-comment" style="margin-left:10px"></span>' \
              + '<span class="glyphicon glyphicon-thumbs-up" style="margin-left:10px"></span>'\
              + "</div>"
        html += ele
        html += render_tree_node(v,margin_val+10)
    return html
def render_comment_tree(tree_dic):
    html = ""
    for k,v in tree_dic.items():
        ele = "<div class='root-comment' comment-id=%s>"%k.id + k.comment+ "<span style='margin-left:10px'>%s</span>"%k.date \
              + "<span style='margin-left:10px'>%s</span>"%k.user.name \
              + '<span class="glyphicon glyphicon-comment add-comment" style="margin-left:10px"></span>' \
              + '<span class="glyphicon glyphicon-thumbs-up " style="margin-left:10px"></span>'\
              + "</div>"
        html += ele
        html += render_tree_node(v,10)
    return html