package com.meeting.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.meeting.model.Credentials;
import com.meeting.model.User;

public interface CredentialsRepository extends JpaRepository<Credentials, Integer>{
	Credentials findByUsername(String username);
}
