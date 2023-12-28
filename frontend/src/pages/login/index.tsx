import React, { useState, useCallback } from 'react';
import { message, Tabs } from 'antd';
import { login } from '@/services/login/api';
import ProForm, { ProFormCheckbox, ProFormText } from '@ant-design/pro-form';
import { FormattedMessage } from 'react-intl';

import styles from './index.less';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import bgImage from '@/assets/backgroud-login.jpeg';

const submitButtonTextMap: Record<string, string> = {
  account: '登录',
  register: '注册',
};

export default function IndexPage() {
  const [type, setType] = useState<string>('account');

  const onSubmit = useCallback((values) => {
    return login(values).then((res) => {
      if (res.success) {
        console.log('go home');
      } else {
        message.error(res.msg);
      }
    });
  }, []);

  return (
    <div
      className={styles.main}
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <div className={styles.form_wrap}>
        <ProForm
          onFinish={onSubmit}
          isKeyPressSubmit
          submitter={{
            render: (_, dom) => dom.pop(),
            searchConfig: {
              submitText: submitButtonTextMap[type],
            },
            submitButtonProps: {
              size: 'large',
              style: {
                width: '100%',
                borderRadius: '32px',
              },
            },
          }}
        >
          <Tabs accessKey={type} onChange={setType}>
            <Tabs.TabPane key="account" tab="账号密码登录" />
            <Tabs.TabPane key="register" tab="注册" />
          </Tabs>
          {/* 登录逻辑 */}
          {type === 'account' && (
            <>
              <ProFormText
                name="username"
                fieldProps={{
                  className: styles.proform_generic_warp,
                  prefix: <UserOutlined className={styles.prefixIcon} />,
                }}
                rules={[
                  {
                    required: true,
                    message: '请输入用户名',
                  },
                ]}
                placeholder="这里输入用户名"
              />

              <ProFormText.Password
                name="password"
                fieldProps={{
                  className: styles.proform_generic_warp,
                  prefix: <LockOutlined className={styles.prefixIcon} />,
                }}
                rules={[
                  {
                    required: true,
                    message: '请输入密码',
                  },
                ]}
                placeholder="这里输入密码"
              />
            </>
          )}
          {/* 注册逻辑 */}
          {type=== 'register' && (
            <>
              <ProFormText
                fieldProps={{
                  className: styles.proform_generic_warp,
                  prefix: <UserOutlined className={styles.prefixIcon} />
                }}
                name="username"
                placeholder='这里输入用户名'
                rules={[
                  {
                    required: true,
                    message: '请输入用户名'
                  }
                ]}
              />

            </>
          )}


          <div className={styles.forget_pwd_wrap}>
            <a
              onClick={() => {
                alert('请联系管理员修改密码');
              }}
            >
              忘记密码？
            </a>
          </div>
        </ProForm>
      </div>
    </div>
  );
}
