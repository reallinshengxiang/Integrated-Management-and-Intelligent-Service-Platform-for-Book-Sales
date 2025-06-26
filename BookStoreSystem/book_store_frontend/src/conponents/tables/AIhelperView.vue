<template>
    <el-card class="box-card ai-helper-card">
        <template #header>
            <div class="card-header">
                <span>小助手</span>
            </div>
        </template>
        <el-col class="input-section">
            <el-input v-model="userInput" placeholder="请输入您的问题" @keyup.enter="sendMessage"></el-input>
            <el-button @click="sendMessage">发送</el-button>
            <el-button @click="clearMessages">清空记录</el-button>
        </el-col>
        <div class="message-container">
            <el-card v-for="(msg, index) in messages" :key="index" class="message-card" :class="{ 'user-message': msg.sender === '用户', 'ai-message': msg.sender === 'AI', 'system-message': msg.sender === '系统' }">
                <template #header>
                    <div class="message-header">
                        <span>{{ msg.sender }}</span>
                    </div>
                </template>
                <p>{{ msg.content }}</p>
            </el-card>
        </div>
    </el-card>
</template>

<script setup>
import { ref } from 'vue';
import { deepseek } from '@/api/index';

const userInput = ref('');
const messages = ref([
    { sender: '系统', content: '您好！有什么可以帮助您的？' }
]);

const clearMessages = () => {
    messages.value = [
        { sender: '系统', content: '您好！有什么可以帮助您的？' }
    ];
};

const sendMessage = async () => {
    if (userInput.value.trim()) {
        messages.value.push({ sender: '用户', content: userInput.value });
        try {
            const response = await deepseek(userInput.value).get();
            messages.value.push({ sender: 'AI', content: response.data.response });
        } catch (error) {
            messages.value.push({ sender: '系统', content: '系统繁忙，请稍后再试。' });
        }
        userInput.value = '';
    }
};
</script>

<style lang="scss" scoped>
.ai-helper-card {
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;

    .card-header {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
    }
}

.input-section {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;

    .el-input {
        flex: 1;
    }
}

.message-container {
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);

    .message-card {
        margin-bottom: 15px;
        border-radius: 8px;
        transition: transform 0.2s ease-in-out;

        &:hover {
            transform: translateY(-3px);
        }

        .message-header {
            font-weight: bold;
            margin-bottom: 5px;
        }
    }

    .user-message {
        background-color: #e1f5fe;
        border: 1px solid #b3e5fc;
    }

    .ai-message {
        background-color: #f1f8e9;
        border: 1px solid #dcedc8;
    }

    .system-message {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
    }
}
</style>