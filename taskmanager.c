#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct Task {
    int id;
    char description[100];
    int priority;  // Priority field
    struct Task* prev;
    struct Task* next;
} Task;
// Function to create a new task
Task* createTask(int id, const char* description, int priority) {
    Task* newTask = (Task*)malloc(sizeof(Task));
    if (newTask == NULL) {
        perror("Memory allocation error");
        exit(1);
    }
    newTask->id = id;
    strncpy(newTask->description, description, sizeof(newTask->description));
    newTask->priority = priority;
    newTask->prev = NULL;
    newTask->next = NULL;
    return newTask;
}

// Function to add a task to the task list based on priority
void addTask(Task** head, Task* newTask) {
    if (*head == NULL) {
        *head = newTask;
    } else {
        Task* current = *head;

        while (current != NULL && newTask->priority >= current->priority) {
            current = current->next;
        }

        if (current == *head) {
            newTask->next = *head;
            (*head)->prev = newTask;
            *head = newTask;
        } else if (current == NULL) {
            Task* last = *head;
            while (last->next != NULL) {
                last = last->next;
            }
            last->next = newTask;
            newTask->prev = last;
        } else {
            newTask->next = current;
            newTask->prev = current->prev;
            current->prev->next = newTask;
            current->prev = newTask;
        }
    }
}

// Function to display the list of tasks
void displayTasks(Task* head) {
    Task* current = head;
    while (current != NULL) {
        printf("Task %d (Priority %d): %s\n", current->id, current->priority, current->description);
        current = current->next;
    }
}

int main() {
    Task* taskList[30] = {NULL}; // Array of task lists, one for each date
    int dat, d;

    printf(" BOSS! How many dates do you want to assign tasks: ");
    scanf("%d", &dat);

    for (int i = 0; i < dat; i++) {
        printf("\n\nEnter the date you want to assign tasks to: ");
        scanf("%d", &d);

        int len, prio;
        char st[100];

        printf("\n\nEnter the number of tasks for date %d: ", d);
        scanf("%d", &len);

        for (int j = 1; j <= len; j++) {
            printf("Enter the name for task %d: ", j);
            scanf("%s", st);
            printf("Gimme the priority for task %d: ", j);
            scanf("%d", &prio);
            addTask(&taskList[d], createTask(j, st, prio));
        }
    }

    // Display the list of tasks with priorities
    int ir = 1;
    while (ir) {
        printf("\n\nWhich date's task list do you want to view: ");
        scanf("%d", &d);
        printf("List of tasks for date %d:\n", d);
        displayTasks(taskList[d]);
        
        // Free memory when done
        Task* current = taskList[d];
        while (current != NULL) {
            Task* temp = current;
            current = current->next;
            free(temp);
        }
        
        printf("\nDo you want to continue? Enter 0 to exit: ");
        scanf("%d", &ir);
    }

    return 0;
}
