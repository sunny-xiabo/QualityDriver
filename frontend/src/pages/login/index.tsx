import React, { useState, useCallback } from 'react';
import { message, Tabs } from 'antd';
import { login } from '@/services/login/api';
import ProForm, { ProFormText } from '@ant-design/pro-form';
import { FormattedMessage } from 'react-intl';

import styles from './index.less';
import { LockOutlined, UserOutlined } from '@ant-design/icons';

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
    <div className={styles.main}>
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
              widows: '100%',
              borderRadius: '32px',
            },
          },
        }}
      >
        <Tabs accessKey={type} onChange={setType}>
          <Tabs.TabPane key="account" tab="账号密码登录" />
          <Tabs.TabPane key="register" tab="注册" />
        </Tabs>

        {type === 'account' && (
          <>
            <ProFormText
              name="username"
              fieldProps={{
                size: 'large',
                style: { borderRadius: '24px' },
                prefix: <UserOutlined className={styles.prefixIcon} />,
              }}
              rules={[
                {
                  required: true,
                  message: <FormattedMessage defaultMessage="请输入用户名!" />,
                },
              ]}
              placeholder="请输入用户名"
            />

            <ProFormText.Password
              name="password"
              fieldProps={{
                size: 'large',
                style: { borderRadius: '24px' },
                prefix: <LockOutlined className={styles.prefixIcon} />,
              }}
              rules={[
                {
                  required: true,
                  message: <FormattedMessage defaultMessage="请输入密码!" />,
                },
              ]}
              placeholder="请输入密码"
            />
          </>
        )}
        <div
          style={{
            marginBottom: 24,
          }}
        ></div>
      </ProForm>
    </div>
  );
}
