import React, { useState, useCallback } from 'react';
import { message } from 'antd';
import { login } from '@/services/login/api';

import styles from './index.less';

export default function IndexPage() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const onSubmit = useCallback(() => {
    login({
      username,
      password,
    }).then((res) => {
      if (res.success) {
        console.log('go home');
      } else {
        message.error(res.msg);
      }
    });
  }, [username, password]);

  return (
    <div>
      
    </div>
  );
}
