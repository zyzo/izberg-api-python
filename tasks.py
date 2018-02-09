# -*- coding: utf-8 -*-

from invoke import task

@task
def currentBranchAsTag(ctx, branch_name=None, config_file='bumpr.rc'):
    # don't put at module level to avoid the requirements for other tasks
    from bumpr.config import Config
    from bumpr.releaser import Releaser
    import os

    if not branch_name:
        branch_name = os.environ.get('TRAVIS_BRANCH', None)
    if not branch_name:
        ret = ctx.run(
            'git rev-parse --abbrev-ref HEAD | grep -v ^HEAD$ || '
            'git rev-parse HEAD'
        )
        if not ret.ok:
            raise RuntimeError("Can't get current branch")
        branch_name = ret.stdout.replace('\n', '')
    config = Config()
    config.override_from_config(config_file)
    releaser = Releaser(config)
    releaser.bump_files([(str(releaser.version), branch_name)])
