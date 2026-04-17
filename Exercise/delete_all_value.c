#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int* data;
    int length;
    int capacity;
} listNode;

bool initList(listNode* list, int capacity) {
    list->data = (int*)malloc(capacity * sizeof(int));
    if (!list->data) return false;
    list->length = 0;
    list->capacity = capacity;
    return true;
}

void destroyList(listNode* list) {
    if (list->data) {
        free(list->data);
        list->data = NULL;
        list->length = 0;
        list->capacity = 0;
    }
}

bool addElement(listNode* list, int value) {
    if (list->length >= list->capacity) {
        printf("List is full");
        return false;
    }
    list->data[list->length] = value;
    list->length++;
    return true;
}

void deleteAllValue(listNode* list,int value) {
    if (list->length == 0) {
        printf("List is none");
        return;
    }

    int count = 0;
    for (int i = 0; i < list->length; i++) {
        if (list->data[i] != value) {
            list->data[count] = list->data[i];
            count++;
        }
    }

    list->length = count;

}

// 打印线性表的所有元素和信息
void printList(listNode* list) {
    printf("线性表: [");                    // 输出左括号
    for (int i = 0; i < list->length; i++) { // 遍历所有元素
        printf("%d", list->data[i]);        // 输出当前元素的值
        if (i < list->length - 1) printf(", ");  // 如果不是最后一个元素，输出逗号分隔
    }
    printf("]\n");                          // 输出右括号并换行
    printf("长度: %d, 容量: %d\n", list->length, list->capacity);  // 输出长度和容量信息
}

int main() {
    system("chcp 65001");
    listNode list;                          // 声明一个顺序表变量

    // 初始化线性表
    if (initList(&list, 10)) {              // 调用初始化函数，容量设为10
        printf("=== 初始化线性表 ===\n");   // 输出提示信息
    }

    // 添加测试数据（包含多个3）
    printf("\n=== 添加元素 ===\n");         // 输出分隔信息和标题
    addElement(&list, 1);                   // 添加元素1
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 2);                   // 添加元素2
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 4);                   // 添加元素4
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 5);                   // 添加元素5
    printList(&list);                       // 打印删除前的线性表状态

    // 删除所有值为3的元素
    int x = 3;                              // 要删除的目标值
    printf("\n=== 删除所有值为 %d 的元素 ===\n", x);  // 输出分隔信息和标题
    deleteAllValue(&list, x);                   // 调用删除函数
    printList(&list);                       // 打印删除后的线性表状态

    // 测试删除不存在的值
    x = 9;                                  // 要删除的目标值（不存在）
    printf("\n=== 删除所有值为 %d 的元素 ===\n", x);  // 输出分隔信息和标题
    deleteAllValue(&list, x);                   // 调用删除函数
    printList(&list);                       // 打印删除后的线性表状态

    // 销毁线性表
    destroyList(&list);                     // 调用销毁函数，释放内存
    printf("线性表已销毁\n");               // 输出销毁信息

    return 0;                               // 主函数正常结束，返回0
}

