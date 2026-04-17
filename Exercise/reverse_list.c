#include <stdio.h>      // 引入标准输入输出库
#include <stdlib.h>     // 引入标准库，包含malloc、free等函数
#include <stdbool.h>    // 引入布尔类型支持

// 定义顺序表结构体
typedef struct {
    int* data;          // 指向动态数组的指针，用于存储元素
    int length;         // 当前顺序表的长度（实际元素个数）
    int capacity;       // 顺序表的容量（最大可容纳元素个数）
} listNode;

bool initList(listNode* list, int capacity) {
    list->data = (int*)malloc(capacity * sizeof(int));
    if (!list->data) return false;
    list->length = 0;
    list->capacity = capacity;
    return true;
}

bool destroyList(listNode* list) {
    if (list->data) {
        free(list->data);
        list->data = NULL;
    }
    list->length = 0;
    list->capacity = 0;
}

bool addElement(listNode* list, int value) {
    if (list->length >= list->capacity) {
        printf("List Is Full\n");
        return false;
    }
    list->data[list->length] = value;
    list->length++;
    return true;
}

void reverseList(listNode* list) {
    if (list->length <= 1) {
        return;
    }

    int temp;
    int left = 0;
    int right = list->length - 1;

    while (left < right) {
        temp = list->data[left];
        list->data[left] = list->data[right];
        list->data[right] = temp;

        left++;
        right--;
    }
}

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

    // 添加测试数据
    printf("\n=== 添加元素 ===\n");         // 输出分隔信息和标题
    addElement(&list, 1);                   // 添加元素1
    addElement(&list, 2);                   // 添加元素2
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 4);                   // 添加元素4
    addElement(&list, 5);                   // 添加元素5
    printList(&list);                       // 打印逆置前的线性表状态

    // 逆置顺序表
    printf("\n=== 逆置顺序表 ===\n");       // 输出分隔信息和标题
    reverseList(&list);                     // 调用逆置函数
    printList(&list);                       // 打印逆置后的线性表状态

    // 再次逆置，恢复原状
    printf("\n=== 再次逆置顺序表 ===\n");   // 输出分隔信息和标题
    reverseList(&list);                     // 再次调用逆置函数
    printList(&list);                       // 打印再次逆置后的线性表状态

    // 销毁线性表
    destroyList(&list);                     // 调用销毁函数，释放内存
    printf("线性表已销毁\n");               // 输出销毁信息

    return 0;                               // 主函数正常结束，返回0
}
