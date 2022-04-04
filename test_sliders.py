from task_presentor import TaskPresentor

def main():

    tp = TaskPresentor("9999", task_list=["emotional_anticipation", "end"], run_task_list=False, practice=True)
    tp.task_obj.run_affect_prompt()


if __name__ == "__main__":
    main()
