import sublime
import sublime_plugin
import subprocess
import os

class CodeTerminalCommand(sublime_plugin.WindowCommand):

    previous = ""

    print("............::::::::| CodeTerminal | Started |::::::::............")

    def run(self):
        sublime.active_window().show_input_panel('Command', self.previous, self.cmd, 'None', 'None')

    def cmd(self, query):

        self.previous = query

        panel = sublime.active_window().create_output_panel("xxx")
        sublime.active_window().run_command("show_panel", {"panel": "output." + "xxx"})
        
        sublime.status_message('CodeTermial | Running command')

        try:
            current_local = os.getcwd()
            os.chdir(sublime.active_window().extract_variables()['folder'])
         
            results, errors = subprocess.Popen(query, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

            if errors:
                result = errors.decode('utf-8', 'replace').replace('b\"\'"', '').replace('\n', ' \n ')

            else:
                result = results.decode('utf-8', 'replace').replace('b\"\'"', '').replace('\n', ' \n ')

            panel.set_read_only(False)
            panel.run_command('append', {'characters': " [Output]\n"})
            panel.run_command('append', {'characters': " =====\n"})
            panel.run_command('append', {'characters': "\n "})
            panel.run_command('append', {'characters': result})
            panel.run_command('append', {'characters': "\n [Finished]"})
            panel.set_read_only(True)
            
            os.chdir(current_local)
        except Exception as error:
            print(error)
