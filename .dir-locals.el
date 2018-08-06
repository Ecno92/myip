((nil . (
         (python-sort-imports-on-save t)
         (flycheck-flake8rc . "setup.cfg")
         (eval . (use-package pipenv
                   :hook (python-mode . pipenv-mode)
                   :init
                   (setq
                    pipenv-projectile-after-switch-function
                    #'pipenv-projectile-after-switch-default))
               )
         )
      ))
