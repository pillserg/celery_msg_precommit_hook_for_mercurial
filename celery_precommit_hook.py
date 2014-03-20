from itertools import chain


def append_celery_to_commit_msg_if_tasks_were_modified(repo, **kwargs):
    commitctx = repo.commitctx

    def rewrite_ctx(ctx, error):
        tasks_dir = 'uaprom/tasks'
        tasks_changed = [
            f_name for f_name in chain(*ctx.status())
            if tasks_dir in f_name
        ]

        if tasks_changed and u'celery' not in ctx._text:
            ctx._text = u"{old_msg} [celery]".format(old_msg=ctx._text)
            print(
                u'\n-----Warn-----\n'
                u'[celery] postfix was auto appended '
                u'to commit msg due to changes in: {0}'.format(tasks_changed)
            )

        return commitctx(ctx, error)

    repo.commitctx = rewrite_ctx
