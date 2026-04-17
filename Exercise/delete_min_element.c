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
        printf("线性表已满，无法插入\n");    // 输出错误信息
        return false;                       // 插入失败，返回false
    }
    list->data[list->length] = value;       // 在表尾位置存入新元素
    list->length++;                         // 长度加1
    return true;                            // 插入成功，返回true
}

// 删除最小值元素并返回其值
bool deleteMin(listNode* list, int* minValue) {
    // 检查顺序表是否为空
    if (list->length == 0) {                // 如果长度为0，说明是空表
        printf("错误：顺序表为空，无法删除\n");  // 输出错误信息
        exit(1);                            // 异常退出程序，返回码1
    }

    // 查找最小值及其位置
    int minPos = 0;                         // 初始化最小值位置为0
    *minValue = list->data[0];              // 初始化最小值为第一个元素
    for (int i = 1; i < list->length; i++) { // 从第二个元素开始遍历
        if (list->data[i] < *minValue) {    // 如果当前元素比最小值还小
            *minValue = list->data[i];      // 更新最小值
            minPos = i;                     // 更新最小值的位置
        }
    }

    // 用最后一个元素填补空出的位置
    list->data[minPos] = list->data[list->length - 1];  // 将最后一个元素复制到最小值位置
    list->length--;                         // 长度减1，相当于删除了最后一个重复元素

    return true;                            // 删除成功，返回true
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

    // 添加测试数据
    printf("\n=== 添加元素 ===\n");         // 输出分隔信息和标题
    addElement(&list, 5);                   // 添加元素5
    addElement(&list, 3);                   // 添加元素3
    addElement(&list, 8);                   // 添加元素8
    addElement(&list, 1);                   // 添加元素1
    addElement(&list, 9);                   // 添加元素9
    addElement(&list, 6);                   // 添加元素6
    printList(&list);                       // 打印当前线性表状态

    // 删除最小值元素
    printf("\n=== 删除最小值元素 ===\n");   // 输出分隔信息和标题
    int minValue;                           // 声明变量用于接收被删除的最小值
    if (deleteMin(&list, &minValue)) {      // 调用删除最小值函数，传入地址
        printf("被删除的最小值是: %d\n", minValue);  // 输出被删除的最小值
    }
    printList(&list);                       // 打印删除后的线性表状态

    // 再次删除最小值
    printf("\n=== 再次删除最小值元素 ===\n");  // 输出分隔信息和标题
    if (deleteMin(&list, &minValue)) {      // 再次调用删除最小值函数
        printf("被删除的最小值是: %d\n", minValue);  // 输出被删除的最小值
    }
    printList(&list);                       // 打印删除后的线性表状态

    // 测试空表情况（注释掉，避免程序退出）
    // printf("\n=== 测试空表删除 ===\n");
    // while (list.length > 0) {
    //     deleteMin(&list, &minValue);
    // }
    // deleteMin(&list, &minValue); // 这会触发错误退出

    // 销毁线性表
    destroyList(&list);                     // 调用销毁函数，释放内存
    printf("线性表已销毁\n");               // 输出销毁信息

    return 0;                               // 主函数正常结束，返回0
}