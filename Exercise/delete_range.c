#include <stdio.h>      // 引入标准输入输出库
#include <stdlib.h>     // 引入标准库，包含malloc、free、exit等函数
#include <stdbool.h>    // 引入布尔类型支持

// 定义顺序表结构体
typedef struct {
    int* data;          // 指向动态数组的指针，用于存储元素
    int length;         // 当前顺序表的长度（实际元素个数）
    int capacity;       // 顺序表的容量（最大可容纳元素个数）
} listNode;

// 初始化线性表函数
bool initList(listNode* list, int capacity) {
    list->data = (int*)malloc(capacity * sizeof(int));  // 动态分配内存，创建大小为capacity的整型数组
    if (!list->data) return false;                      // 如果内存分配失败，返回false
    list->length = 0;                                   // 初始化长度为0，表示空表
    list->capacity = capacity;                          // 设置容量为指定值
    return true;                                        // 初始化成功，返回true
}

// 销毁线性表函数
void destroyList(listNode* list) {
    if (list->data) {                   // 如果data指针不为空
        free(list->data);               // 释放动态分配的数组内存
        list->data = NULL;              // 将指针置为空，避免野指针
    }
    list->length = 0;                   // 重置长度为0
    list->capacity = 0;                 // 重置容量为0
}

// 添加元素到顺序表末尾
bool addElement(listNode* list, int value) {
    if (list->length >= list->capacity) {   // 检查是否已满
        printf("Error: List is full\n");    // 输出错误信息
        return false;                       // 插入失败，返回false
    }
    list->data[list->length] = value;       // 在表尾位置存入新元素
    list->length++;                         // 长度加1
    return true;                            // 插入成功，返回true
}

void deleteRange(listNode* list, int s, int t) {
    if (s >= t) {
        printf("Error: Invalid parameters, require s < t\n");
        exit(1);
    }

    if (list->length == 0) {
        printf("Error: List is empty\n");
        exit(1);
    }

    int count = 0;
    for (int i = 0; i < list->length; i++) {
        if (list->data[i] < s || list->data[i] > t) {
            list->data[count] = list->data[i];
            count++;
        }
    }

    list->length = count;

}

// 打印线性表的所有元素和信息
void printList(listNode* list) {
    printf("List: [");                      // 输出左括号
    for (int i = 0; i < list->length; i++) { // 遍历所有元素
        printf("%d", list->data[i]);        // 输出当前元素的值
        if (i < list->length - 1) printf(", ");  // 如果不是最后一个元素，输出逗号分隔
    }
    printf("]\n");                          // 输出右括号并换行
    printf("Length: %d, Capacity: %d\n", list->length, list->capacity);  // 输出长度和容量信息
}

int main() {
    system("chcp 65001");
    listNode list;                          // 声明一个顺序表变量

    // 初始化线性表
    if (initList(&list, 10)) {              // 调用初始化函数，容量设为10
        printf("=== Initialize List ===\n");   // 输出提示信息
    }

    // 添加测试数据
    printf("\n=== Add Elements ===\n");     // 输出分隔信息和标题
    addElement(&list, 1);                   // 添加元素1
    addElement(&list, 5);                   // 添加元素5
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 7);                   // 添加元素7
    addElement(&list, 2);                   // 添加元素2
    addElement(&list, 8);                   // 添加元素8
    addElement(&list, 4);                   // 添加元素4
    addElement(&list, 6);                   // 添加元素6
    printList(&list);                       // 打印删除前的线性表状态

    // 删除值在[3, 6]范围内的元素
    int s = 3, t = 6;                       // 定义范围[s, t]
    printf("\n=== Delete elements in range [%d, %d] ===\n", s, t);  // 输出分隔信息和标题
    deleteRange(&list, s, t);               // 调用删除函数
    printList(&list);                       // 打印删除后的线性表状态

    // 测试参数不合法的情况（注释掉，避免程序退出）
    // printf("\n=== Test invalid parameters s >= t ===\n");
    // deleteRange(&list, 5, 3);            // s > t，会触发错误退出

    // 测试空表情况（注释掉，避免程序退出）
    // printf("\n=== Test empty list deletion ===\n");
    // while (list.length > 0) {
    //     list.length--;
    // }
    // deleteRange(&list, 1, 5);            // 空表，会触发错误退出

    // 销毁线性表
    destroyList(&list);                     // 调用销毁函数，释放内存
    printf("List destroyed\n");             // 输出销毁信息

    return 0;                               // 主函数正常结束，返回0
}
