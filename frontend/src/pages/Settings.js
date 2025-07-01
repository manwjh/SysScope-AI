import React, { useState } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Button, 
  Switch, 
  InputNumber, 
  Select,
  Divider,
  message,
  Alert,
  Space
} from 'antd';
import { SaveOutlined, ReloadOutlined } from '@ant-design/icons';
import { saveSettings } from '../utils/api';

const { Option } = Select;

const Settings = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSave = async (values) => {
    try {
      setLoading(true);
      // 映射前端字段为后端config.env格式
      const payload = {
        LLM_PROVIDER: values.llm_provider,
        LLM_MODEL: values.llm_model,
        LLM_API_KEY: values.llm_api_key,
        LLM_BASE_URL: values.llm_base_url,
        LLM_MAX_TOKENS: values.llm_max_tokens,
        LLM_TEMPERATURE: values.llm_temperature,
        REPORT_OUTPUT_PATH: values.report_output_path,
        REPORT_FILENAME_PATTERN: values.report_filename_pattern,
        REPORT_INCLUDE_SYSTEM_INFO: values.report_include_system_info,
        REPORT_INCLUDE_RAW_LOGS: values.report_include_raw_logs,
        REPORT_INCLUDE_ANALYSIS: values.report_include_analysis
      };
      await saveSettings(payload);
      message.success('配置保存成功！请重启后端服务使配置生效。');
    } catch (error) {
      message.error('保存配置失败: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    form.resetFields();
    message.info('配置已重置');
  };

  return (
    <div>
      <Card title="系统设置" extra={
        <Space>
          <Button 
            icon={<ReloadOutlined />}
            onClick={handleReset}
          >
            重置
          </Button>
          <Button 
            type="primary"
            icon={<SaveOutlined />}
            loading={loading}
            onClick={() => form.submit()}
          >
            保存
          </Button>
        </Space>
      }>
        <Alert
          message="配置说明"
          description="以下配置将影响LLM API调用和报告生成。修改后需要重启应用才能生效。"
          type="info"
          showIcon
          style={{ marginBottom: 24 }}
        />

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            llm_provider: 'custom',
            llm_model: 'doubao-seed-1-6-flash-250615',
            llm_api_key: '',
            llm_base_url: 'https://ark.cn-beijing.volces.com/api/v3',
            llm_max_tokens: 4000,
            llm_temperature: 0.7,
            report_output_path: 'reports',
            report_filename_pattern: 'report_{timestamp}_{system_name}',
            report_include_system_info: true,
            report_include_raw_logs: false,
            report_include_analysis: true
          }}
        >
          <Divider orientation="left">LLM API配置</Divider>
          
          <Form.Item
            name="llm_provider"
            label="LLM提供商"
            rules={[{ required: true, message: '请选择LLM提供商' }]}
          >
            <Select>
              <Option value="custom">自定义API</Option>
              <Option value="openai">OpenAI</Option>
              <Option value="anthropic">Anthropic</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="llm_model"
            label="模型名称"
            rules={[{ required: true, message: '请输入模型名称' }]}
          >
            <Input placeholder="例如: doubao-seed-1-6-flash-250615" />
          </Form.Item>

          <Form.Item
            name="llm_api_key"
            label="API密钥"
            rules={[{ required: true, message: '请输入API密钥' }]}
          >
            <Input.Password placeholder="请输入API密钥" />
          </Form.Item>

          <Form.Item
            name="llm_base_url"
            label="API基础URL"
            rules={[{ required: true, message: '请输入API基础URL' }]}
          >
            <Input placeholder="例如: https://ark.cn-beijing.volces.com/api/v3" />
          </Form.Item>

          <Form.Item
            name="llm_max_tokens"
            label="最大Token数"
            rules={[{ required: true, message: '请输入最大Token数' }]}
          >
            <InputNumber min={1} max={8000} style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="llm_temperature"
            label="温度参数"
            rules={[{ required: true, message: '请输入温度参数' }]}
          >
            <InputNumber min={0} max={2} step={0.1} style={{ width: '100%' }} />
          </Form.Item>

          <Divider orientation="left">报告配置</Divider>

          <Form.Item
            name="report_output_path"
            label="报告输出路径"
            rules={[{ required: true, message: '请输入报告输出路径' }]}
          >
            <Input placeholder="例如: reports" />
          </Form.Item>

          <Form.Item
            name="report_filename_pattern"
            label="文件名模式"
            rules={[{ required: true, message: '请输入文件名模式' }]}
          >
            <Input placeholder="例如: report_{timestamp}_{system_name}" />
          </Form.Item>

          <Form.Item
            name="report_include_system_info"
            label="包含系统信息"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="report_include_raw_logs"
            label="包含原始日志"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            name="report_include_analysis"
            label="包含LLM分析"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Settings;
