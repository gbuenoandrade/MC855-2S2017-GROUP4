import os


class Hadoop:
    def __init__(self, hdfs_folder):
        self.hdfs_folder = hdfs_folder

    def _execute_sys_calls(self, input_path):
        os.system('rm -rf hadoop/output')
        os.system('hadoop fs -rm input.txt')
        os.system('hadoop fs -rm -r output')
        os.system('hadoop fs -copyFromLocal %s %s' % (input_path, self.hdfs_folder))
        os.system('hadoop jar hadoop/hadoop-streaming-2.8.0.jar '
                  '-mapper hadoop/mapper.py -reducer hadoop/reducer.py -input input.txt -output output')
        os.system('hadoop fs -copyToLocal %s/output hadoop/output' % self.hdfs_folder)

    def _get_and_delete_output(self):
        ans = []
        for filename in os.listdir('hadoop/output'):
            if filename.startswith('part'):
                with open('hadoop/output/' + filename, 'r') as f:
                    lines = [line.rstrip('\n') for line in f]
                    ans += lines
        os.system('rm -rf hadoop/output')
        return ans

    def run(self, input_path):
        self._execute_sys_calls(input_path)
        output = self._get_and_delete_output()
        return output
