from task_presentor import TaskPresentor

def main():

    tp = TaskPresentor("9999", task_list=["affect_reading", "end"] ,run_task_list=False)
    tp.task_obj.run_slider_tut()


if __name__ == "__main__":
    main()
