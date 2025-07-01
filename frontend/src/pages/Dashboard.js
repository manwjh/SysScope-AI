import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Statistic, 
  Button, 
  Progress, 
  Descriptions, 
  Alert,
  Spin,
  message,
  Table,
  Tag
} from 'antd';
import { 
  DesktopOutlined, 
  ExperimentOutlined, 
  FileTextOutlined, 
  CheckCircleOutlined,
  ClockCircleOutlined 
} from '@ant-design/icons';
import { getSystemInfo, generateTestPlan, executeTests } from '../utils/api';
import axios from 'axios';

const Dashboard = () => {
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [testPlan, setTestPlan] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [showTestProgress, setShowTestProgress] = useState(false);
  const [testProgress, setTestProgress] = useState([]);

  useEffect(() => {
    loadSystemInfo();
    // 只有在显示测试进度时才轮询
    let timer;
    if (showTestProgress) {
      timer = setInterval(() => {
        fetchTestProgress();
      }, 2000);
    }
    return () => timer && clearInterval(timer);
  }, [showTestProgress]);

  const loadSystemInfo = async () => {
    try {
      setLoading(true);
      const data = await getSystemInfo();
      setSystemInfo(data);
    } catch (error) {
      message.error('获取系统信息失败: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateTestPlan = async () => {
    try {
      setGenerating(true);
      const plan = await generateTestPlan();
      setTestPlan(plan);
      message.success('测试计划生成成功！');
    } catch (error) {
      message.error('生成测试计划失败: ' + error.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleExecuteTests = async () => {
    if (!testPlan) {
      message.warning('请先生成测试计划');
      return;
    }
    try {
      setExecuting(true);
      // 初始化进度栏为本次测试项目，全部pending
      setTestProgress(
        testPlan.test_items.map(item => ({
          name: item.name,
          status: 'pending',
          progress: 0,
          result: null,
        }))
      );
      setShowTestProgress(true);
      await executeTests(testPlan);
      message.success('测试已开始执行！');
    } catch (error) {
      message.error('执行测试失败: ' + error.message);
      setShowTestProgress(false);
    } finally {
      setExecuting(false);
    }
  };

  const fetchTestProgress = async () => {
    try {
      const res = await axios.get('/api/test/progress');
      setTestProgress(res.data);
      // 如果所有测试都已完成或失败，则自动隐藏进度栏
      if (Array.isArray(res.data) && res.data.length > 0) {
        const allDone = res.data.every(item => ['completed', 'failed', 'skipped'].includes(item.status));
        if (allDone) setShowTestProgress(false);
      }
    } catch (e) {
      // 忽略错误
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>正在加载系统信息...</div>
      </div>
    );
  }

  if (!systemInfo) {
    return (
      <Alert
        message="系统信息获取失败"
        description="无法获取系统信息，请检查后端服务是否正常运行。"
        type="error"
        showIcon
      />
    );
  }

  const memoryUsage = ((systemInfo.memory_total - systemInfo.memory_available) / systemInfo.memory_total) * 100;

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

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="系统概览">
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Statistic
                  title="系统平台"
                  value={systemInfo.platform}
                  prefix={<DesktopOutlined />}
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="CPU核心数"
                  value={systemInfo.cpu_count}
                  suffix="核"
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="总内存"
                  value={(systemInfo.memory_total / (1024**3)).toFixed(1)}
                  suffix="GB"
                />
              </Col>
              <Col span={6}>
                <Statistic
                  title="主机名"
                  value={systemInfo.hostname}
                />
              </Col>
            </Row>
          </Card>
        </Col>

        <Col span={12}>
          <Card title="内存使用情况">
            <Progress
              type="dashboard"
              percent={memoryUsage.toFixed(1)}
              format={percent => `${percent}%`}
              status={memoryUsage > 80 ? 'exception' : 'normal'}
            />
            <Descriptions column={1} size="small" style={{ marginTop: 16 }}>
              <Descriptions.Item label="总内存">
                {(systemInfo.memory_total / (1024**3)).toFixed(1)} GB
              </Descriptions.Item>
              <Descriptions.Item label="可用内存">
                {(systemInfo.memory_available / (1024**3)).toFixed(1)} GB
              </Descriptions.Item>
              <Descriptions.Item label="已用内存">
                {((systemInfo.memory_total - systemInfo.memory_available) / (1024**3)).toFixed(1)} GB
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </Col>

        <Col span={12}>
          <Card title="系统信息详情">
            <Descriptions column={1} size="small">
              <Descriptions.Item label="操作系统">
                {systemInfo.system} {systemInfo.release}
              </Descriptions.Item>
              <Descriptions.Item label="处理器">
                {systemInfo.processor}
              </Descriptions.Item>
              <Descriptions.Item label="机器类型">
                {systemInfo.machine}
              </Descriptions.Item>
              <Descriptions.Item label="用户名">
                {systemInfo.username}
              </Descriptions.Item>
              <Descriptions.Item label="检测时间">
                {new Date(systemInfo.detected_at).toLocaleString()}
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </Col>

        <Col span={24}>
          <Card title="快速操作">
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Button 
                  icon={<FileTextOutlined />}
                  block
                  onClick={() => window.location.href = '/reports'}
                >
                  查看报告
                </Button>
              </Col>
              <Col span={6}>
                <Button 
                  icon={<ClockCircleOutlined />}
                  block
                  onClick={loadSystemInfo}
                >
                  刷新信息
                </Button>
              </Col>
              <Col span={6}>
                <Button 
                  icon={<ExperimentOutlined />}
                  block
                  loading={generating}
                  onClick={handleGenerateTestPlan}
                >
                  生成测试计划
                </Button>
              </Col>
              <Col span={6}>
                <Button 
                  type="primary"
                  icon={<CheckCircleOutlined />}
                  block
                  loading={executing}
                  onClick={handleExecuteTests}
                  disabled={!testPlan}
                >
                  执行测试
                </Button>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      {/* 测试进度与结果栏目，仅在 showTestProgress 时显示 */}
      {showTestProgress && (
        <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
          <Col span={24}>
            <Card title="测试进度与结果">
              <Table
                columns={testColumns}
                dataSource={testProgress}
                rowKey="name"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default Dashboard;
