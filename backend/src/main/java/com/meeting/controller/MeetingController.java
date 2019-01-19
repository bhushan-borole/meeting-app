package com.meeting.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.meeting.model.Meeting;
import com.meeting.model.User;
import com.meeting.repository.MeetingRepository;
import com.meeting.repository.UserRepository;

@RestController
@RequestMapping("rest")
public class MeetingController {

	@Autowired
	MeetingRepository meetingRepository;
	
	@Autowired
	UserRepository userRepository;

	@CrossOrigin(origins = {"http://localhost:8080"})
	@GetMapping("/meetings")
	public List<Meeting> getAllMeetings() {
		//go to repo and fetch all meetings
		return meetingRepository.findAll();
	}
	 @CrossOrigin(origins = {"http://localhost:8080"})
	 @GetMapping("/meeting/{id}")
	public Meeting getMeeting(@PathVariable("id") int id) {
		//go to repo and fetch meeting based on id
		return meetingRepository.getOne(id);
	}
	 @CrossOrigin(origins = {"http://localhost:8080"})
	 @PostMapping("/meeting/{userid}")
	public Meeting addMeeting(@PathVariable("userid") int userId,@RequestBody Meeting meeting) {
		//go to repo and fetch user details based on userID
		User user=userRepository.getOne(userId);
		
		//go to repo and add meeting in db
		meeting.setUser(user);
		
		return meetingRepository.save(meeting);
	}
	 @CrossOrigin(origins = {"http://localhost:8080"})
	 @PutMapping("/meeting/{id}")
	public Meeting updateMeeting(@PathVariable("id") int id, @RequestBody Meeting meeting) {
		//go to repo and fetch existing meeting based on id
		Meeting m = meetingRepository.getOne(id);
		m.setTitle(meeting.getTitle());
		m.setVenue(meeting.getVenue());
		return meetingRepository.save(m);
		
	}
	 @CrossOrigin(origins = {"http://localhost:8080"})
	 @DeleteMapping("/meeting/{id}")
	public void deleteMeeting(@PathVariable("id") int id) {
		meetingRepository.deleteById(id);
	}
	
	 @CrossOrigin(origins = {"http://localhost:8080"})
	 @PostMapping("/assignTask/{mid}/{tid}")
	public void assignTask(@PathVariable("mid") int mid,
			@PathVariable("tid") int tid){
		meetingRepository.assignTask(mid,tid);
		
	}
}






