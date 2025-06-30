import React, { useState, useEffect } from 'react';
import { 
  Card, 
  List, 
  Button, 
  Space, 
  Modal, 
  message, 
  Empty,
  Tag,
  Typography 
} from 'antd';
import { 
  FileTextOutlined, 
  DownloadOutlined, 
  EyeOutlined,
  DeleteOutlined 
} from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { getReports, getReport } from '../utils/api';

const { Text } = Typography;

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);
  const [reportContent, setReportContent] = useState('');
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await getReports();
      setReports(data.reports || []);
    } catch (error) {
      message.error('加载报告列表失败: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleViewReport = async (reportId) => {
    try {
      const content = await getReport(reportId);
      setReportContent(content);
      setSelectedReport(reports.find(r => r.id === reportId));
      setModalVisible(true);
    } catch (error) {
      message.error('加载报告内容失败: ' + error.message);
    }
  };

  const handleDownloadReport = (report) => {
    const element = document.createElement('a');
    const file = new Blob([reportContent], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `${report.name}`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN');
  };

  return (
    <div>
      <Card title="测试报告" extra={
        <Button 
          icon={<DownloadOutlined />}
          onClick={loadReports}
        >
          刷新列表
        </Button>
      }>
        {reports.length === 0 ? (
          <Empty
            description="暂无测试报告"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        ) : (
          <List
            dataSource={reports}
            loading={loading}
            renderItem={(report) => (
              <List.Item
                actions={[
                  <Button 
                    type="link" 
                    icon={<EyeOutlined />}
                    onClick={() => handleViewReport(report.id)}
                  >
                    查看
                  </Button>,
                  <Button 
                    type="link" 
                    icon={<DownloadOutlined />}
                    onClick={() => handleDownloadReport(report)}
                  >
                    下载
                  </Button>
                ]}
              >
                <List.Item.Meta
                  avatar={<FileTextOutlined style={{ fontSize: 24, color: '#1890ff' }} />}
                  title={
                    <Space>
                      <Text strong>{report.name}</Text>
                      <Tag color="blue">Markdown</Tag>
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size="small">
                      <Text type="secondary">报告ID: {report.id}</Text>
                      <Text type="secondary">路径: {report.path}</Text>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>

      <Modal
        title={`测试报告 - ${selectedReport?.name || ''}`}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        width="80%"
        footer={[
          <Button key="close" onClick={() => setModalVisible(false)}>
            关闭
          </Button>,
          <Button 
            key="download" 
            type="primary" 
            icon={<DownloadOutlined />}
            onClick={() => selectedReport && handleDownloadReport(selectedReport)}
          >
            下载
          </Button>
        ]}
      >
        <div style={{ maxHeight: '60vh', overflow: 'auto' }}>
          <ReactMarkdown>{reportContent}</ReactMarkdown>
        </div>
      </Modal>
    </div>
  );
};

export default Reports;
