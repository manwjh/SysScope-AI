import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  DashboardOutlined, 
  ExperimentOutlined, 
  FileTextOutlined, 
  SettingOutlined 
} from '@ant-design/icons';

const { Header: AntHeader } = Layout;
const { Title } = Typography;

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表板',
    },
    {
      key: '/test-plan',
      icon: <ExperimentOutlined />,
      label: '测试计划',
    },
    {
      key: '/reports',
      icon: <FileTextOutlined />,
      label: '测试报告',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '设置',
    },
  ];

  const handleMenuClick = ({ key }) => {
    navigate(key);
  };

  return (
    <AntHeader style={{ 
      display: 'flex', 
      alignItems: 'center', 
      background: '#fff',
      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      padding: '0 24px'
    }}>
      <Title level={3} style={{ margin: 0, marginRight: 48, color: '#1890ff' }}>
        SysScope AI
      </Title>
      <Menu
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={handleMenuClick}
        style={{ flex: 1, border: 'none' }}
      />
    </AntHeader>
  );
};

export default Header; 