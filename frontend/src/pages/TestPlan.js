import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Button, 
  Table, 
  Switch, 
  Space, 
  message, 
  Descriptions,
  Tag,
  Progress,
  Alert
} from 'antd';
import { 
  PlayCircleOutlined, 
  ExperimentOutlined, 
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined 
} from '@ant-design/icons';
import { generateTestPlan, executeTests } from '../utils/api';
import axios from 'axios';

const TestPlan = () => {
  const [testPlan, setTestPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [executing, setExecuting] = useState(false);
  const [results, setResults] = useState(null);
  const [testProgress, setTestProgress] = useState([]);

  useEffect(() => {
    console.log('TestPlan component mounted');
    console.log('Current testPlan state:', testPlan);
    // 定时轮询测试进度
    const timer = setInterval(() => {
      fetchTestProgress();
    }, 2000);
    return () => clearInterval(timer);
  }, []);

  const fetchTestProgress = async () => {
    try {
      const res = await axios.get('/api/test/progress');
      setTestProgress(res.data);
    } catch (e) {
      // 忽略错误
    }
  };

  const handleGeneratePlan = async () => {
    try {
      console.log('Starting to generate test plan...');
      setLoading(true);
      const plan = await generateTestPlan();
      console.log('Generated test plan:', plan);
      setTestPlan(plan);
      message.success('测试计划生成成功！');
    } catch (error) {
      console.error('Error generating test plan:', error);
      message.error('生成测试计划失败: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteTests = async () => {
    if (!testPlan) {
      message.warning('请先生成测试计划');
      return;
    }

    try {
      setExecuting(true);
      const result = await executeTests(testPlan);
      console.log('Test execution result:', result);
      setResults(result);
      message.success('测试执行完成！');
    } catch (error) {
      message.error('执行测试失败: ' + error.message);
    } finally {
      setExecuting(false);
    }
  };

  const handleToggleTest = (testId, enabled) => {
    if (!testPlan) return;
    
    const updatedTests = testPlan.test_items.map(test => 
      test.id === testId ? { ...test, enabled } : test
    );
    setTestPlan({ ...testPlan, test_items: updatedTests });
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'failed': return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      case 'skipped': return <ClockCircleOutlined style={{ color: '#faad14' }} />;
      default: return <ClockCircleOutlined style={{ color: '#d9d9d9' }} />;
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      'system_info': 'blue',
      'performance': 'green',
      'security': 'red',
      'network': 'cyan',
      'storage': 'orange',
      'software': 'purple',
      'hardware': 'geekblue',
      'custom': 'default'
    };
    return colors[category] || 'default';
  };

  const statusMap = {
    pending: { color: 'default', text: '等待中' },
    running: { color: 'processing', text: '进行中' },
    completed: { color: 'success', text: '成功' },
    failed: { color: 'error', text: '失败' },
    skipped: { color: 'warning', text: '跳过' },
  };

  const testColumns = [
    { title: '测试名称', dataIndex: 'name', key: 'name' },
    { title: '状态', dataIndex: 'status', key: 'status',
      render: status => <Tag color={statusMap[status]?.color}>{statusMap[status]?.text || status}</Tag>
    },
    { title: '进度', dataIndex: 'progress', key: 'progress',
      render: progress => <Progress percent={progress} size="small" />
    },
    { title: '结果', dataIndex: 'result', key: 'result',
      render: result => result ? <Tag color="green">{result}</Tag> : '-'
    },
  ];

  const columns = [
    {
      title: '启用',
      dataIndex: 'enabled',
      key: 'enabled',
      width: 80,
      render: (enabled, record) => (
        <Switch 
          checked={enabled} 
          onChange={(checked) => handleToggleTest(record.id, checked)}
        />
      ),
    },
    {
      title: '测试名称',
      dataIndex: 'name',
      key: 'name',
      render: (name, record) => (
        <div>
          <div style={{ fontWeight: 'bold' }}>{name}</div>
          <div style={{ fontSize: '12px', color: '#666' }}>{record.description}</div>
        </div>
      ),
    },
    {
      title: '类别',
      dataIndex: 'category',
      key: 'category',
      width: 120,
      render: (category) => (
        <Tag color={getCategoryColor(category)}>
          {category.replace('_', ' ').toUpperCase()}
        </Tag>
      ),
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      width: 100,
      render: (priority) => (
        <Tag color={priority >= 4 ? 'red' : priority >= 3 ? 'orange' : 'green'}>
          P{priority}
        </Tag>
      ),
    },
    {
      title: '超时时间',
      dataIndex: 'timeout',
      key: 'timeout',
      width: 100,
      render: (timeout) => `${timeout}s`,
    },
    {
      title: '状态',
      key: 'status',
      width: 100,
      render: (_, record) => {
        if (!results) return '-';
        
        // Handle different possible data structures
        let testResultsArray = null;
        if (results.test_results && Array.isArray(results.test_results.test_results)) {
          testResultsArray = results.test_results.test_results;
        } else if (Array.isArray(results.test_results)) {
          testResultsArray = results.test_results;
        }
        
        if (!testResultsArray) return '-';
        
        const result = testResultsArray.find(r => r.test_item_id === record.id);
        return result ? (
          <Space>
            {getStatusIcon(result.status)}
            {result.status}
          </Space>
        ) : '-';
      },
    },
  ];

  console.log('Rendering TestPlan component, testPlan:', testPlan);

  return (
    <div>
      <Card title="测试进度与结果" style={{ marginBottom: 24 }}>
        <Table
          columns={testColumns}
          dataSource={testProgress}
          rowKey="name"
          pagination={false}
          size="small"
        />
      </Card>
      <Card title="测试计划管理" extra={
        <Space>
          <Button 
            icon={<ExperimentOutlined />}
            loading={loading}
            onClick={handleGeneratePlan}
          >
            生成测试计划
          </Button>
          <Button 
            type="primary"
            icon={<PlayCircleOutlined />}
            loading={executing}
            onClick={handleExecuteTests}
            disabled={!testPlan}
          >
            执行测试
          </Button>
        </Space>
      }>
        {!testPlan ? (
          <Alert
            message="暂无测试计划"
            description="点击'生成测试计划'按钮来创建新的测试计划。"
            type="info"
            showIcon
            action={
              <Button size="small" type="primary" onClick={handleGeneratePlan}>
                生成计划
              </Button>
            }
          />
        ) : (
          <>
            <Descriptions title="测试计划信息" bordered style={{ marginBottom: 16 }}>
              <Descriptions.Item label="计划名称">{testPlan.name}</Descriptions.Item>
              <Descriptions.Item label="计划描述">{testPlan.description}</Descriptions.Item>
              <Descriptions.Item label="测试项目数">{testPlan.test_items.length}</Descriptions.Item>
              <Descriptions.Item label="启用项目数">
                {testPlan.test_items.filter(t => t.enabled).length}
              </Descriptions.Item>
            </Descriptions>

            {results && (
              <Card title="执行结果" style={{ marginBottom: 16 }}>
                <Space size="large">
                  <div>
                    <div>总测试数: {results.test_results?.total_tests || 0}</div>
                    <div>通过: {results.test_results?.passed_tests || 0} ✅</div>
                    <div>失败: {results.test_results?.failed_tests || 0} ❌</div>
                    <div>跳过: {results.test_results?.skipped_tests || 0} ⏭️</div>
                  </div>
                  <div>
                    <Progress
                      type="circle"
                      percent={results.test_results?.total_tests > 0 ? (results.test_results.passed_tests / results.test_results.total_tests) * 100 : 0}
                      format={percent => `${percent.toFixed(1)}%`}
                    />
                  </div>
                </Space>
              </Card>
            )}

            <Table
              columns={columns}
              dataSource={testPlan.test_items}
              rowKey="id"
              pagination={false}
              scroll={{ x: 800 }}
            />
          </>
        )}
      </Card>
    </div>
  );
};

export default TestPlan;
