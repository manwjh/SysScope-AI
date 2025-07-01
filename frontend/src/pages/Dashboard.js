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
  message 
} from 'antd';
import { 
  DesktopOutlined, 
  ExperimentOutlined, 
  FileTextOutlined, 
  CheckCircleOutlined,
  ClockCircleOutlined 
} from '@ant-design/icons';
import { getSystemInfo, generateTestPlan } from '../utils/api';

const Dashboard = () => {
  const [systemInfo, setSystemInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadSystemInfo();
  }, []);

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
      await generateTestPlan();
      message.success('测试计划生成成功！');
    } catch (error) {
      message.error('生成测试计划失败: ' + error.message);
    } finally {
      setGenerating(false);
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
                  icon={<CheckCircleOutlined />}
                  block
                  onClick={() => window.location.href = '/test-plan'}
                >
                  执行测试
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
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
