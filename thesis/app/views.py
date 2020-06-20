from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys
import os
import argparse
import tensorflow as tf
import numpy as np
from . import facenet
from . import detect_face
import random
from time import sleep

from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import *
from .decorators import admin_only
from .forms import *
import errno

from thesis.settings import BASE_DIR
#from . import align_img




######### AI Related Imports
def align(request):
	

	output_dir_path = 'app/processed_image'
	output_dir = os.path.expanduser(output_dir_path)
	if not os.path.exists(output_dir):
			os.makedirs(output_dir)

	datadir = 'app/train_img'
	dataset = facenet.get_dataset(datadir)

	print('Creating networks and loading parameters')
	with tf.Graph().as_default():
		gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
		sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
		with sess.as_default():
			pnet, rnet, onet = detect_face.create_mtcnn(sess, 'app/npy')

	minsize = 20  # minimum size of face
	threshold = [0.6, 0.7, 0.7]  # three steps's threshold
	factor = 0.709  # scale factor
	margin = 44
	image_size = 182

	# Add a random key to the filename to allow alignment using multiple processes
	random_key = np.random.randint(0, high=99999)
	bounding_boxes_filename = os.path.join(output_dir, 'bounding_boxes_%05d.txt' % random_key)
	print('Goodluck')

	with open(bounding_boxes_filename, "w") as text_file:
		nrof_images_total = 0
		nrof_successfully_aligned = 0
		for cls in dataset:
			output_class_dir = os.path.join(output_dir, cls.name)
			if not os.path.exists(output_class_dir):
				os.makedirs(output_class_dir)
			for image_path in cls.image_paths:
				nrof_images_total += 1
				filename = os.path.splitext(os.path.split(image_path)[1])[0]
				output_filename = os.path.join(output_class_dir, filename + '.png')
				print(image_path)
				if not os.path.exists(output_filename):
					try:
						img = misc.imread(image_path)
						print('read data dimension: ', img.ndim)
					except (IOError, ValueError, IndexError) as e:
						errorMessage = '{}: {}'.format(image_path, e)
						print(errorMessage)
					else:
						if img.ndim < 2:
							print('Unable to align "%s"' % image_path)
							text_file.write('%s\n' % (output_filename))
							continue
						if img.ndim == 2:
							img = facenet.to_rgb(img)
							print('to_rgb data dimension: ', img.ndim)
						img = img[:, :, 0:3]
						print('after data dimension: ', img.ndim)

						bounding_boxes, _ = detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
						nrof_faces = bounding_boxes.shape[0]
						print('detected_face: %d' % nrof_faces)
						if nrof_faces > 0:
							det = bounding_boxes[:, 0:4]
							img_size = np.asarray(img.shape)[0:2]
							if nrof_faces > 1:
								bounding_box_size = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
								img_center = img_size / 2
								offsets = np.vstack([(det[:, 0] + det[:, 2]) / 2 - img_center[1],
													(det[:, 1] + det[:, 3]) / 2 - img_center[0]])
								offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
								index = np.argmax(bounding_box_size - offset_dist_squared * 2.0)  # some extra weight on the centering
								det = det[index, :]
							det = np.squeeze(det)
							bb_temp = np.zeros(4, dtype=np.int32)

							bb_temp[0] = det[0]
							bb_temp[1] = det[1]
							bb_temp[2] = det[2]
							bb_temp[3] = det[3]

							cropped_temp = img[bb_temp[1]:bb_temp[3], bb_temp[0]:bb_temp[2], :]
							scaled_temp = misc.imresize(cropped_temp, (image_size, image_size), interp='bilinear')

							nrof_successfully_aligned += 1
							misc.imsave(output_filename, scaled_temp)
							text_file.write('%s %d %d %d %d\n' % (output_filename, bb_temp[0], bb_temp[1], bb_temp[2], bb_temp[3]))
						else:
							print('Unable to align "%s"' % image_path)
							text_file.write('%s\n' % (output_filename))

	print('Total number of images: %d' % nrof_images_total)
	print('Number of successfully aligned images: %d' % nrof_successfully_aligned)
	


	context = {}

	return render(request, 'app/align.html', context)


def upload(request):
	base = BASE_DIR + '/app/train_img/'

	if request.method == 'POST':

		folder = request.POST['name']
		uploaded_file = request.FILES['document']
		path = os.path.join(base, folder)
		print(path)
		try:
			os.mkdir(path)
		except OSError as e:
			if e.errno == errno.EEXIST:
				redirect('app/upload.html')
			else:
				raise

		fs = FileSystemStorage(location=path)
		fs.save(uploaded_file.name, uploaded_file)

	data_dir = base

	for folder in os.listdir(data_dir):
		i = 1
		print(folder)
		fold = data_dir + '/' + folder
		for img in os.listdir(fold):
			extension = img.split(".")[-1].lower()
			# if extension != "jpeg":
			#    continue
			if i == 0:
				stri = '000'
			elif 0 < i < 10:
				stri = '00' + str(i)
			elif 9 < i < 99:
				stri = '0' + str(i)
			else:
				stri = str(i)
			extension = 'jpg'
			os.rename(os.path.join(fold, img), os.path.join(
				fold, os.path.basename(fold) + "_0" + stri + '.' + extension))
			i = i + 1

	return render(request, 'app/upload.html')



#################################################################


################## User Pages #####################

@login_required(login_url='login')
def home(request):

    return render(request, 'app/dashboard.html')

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				print(user)
				username = form.cleaned_data.get('username')
				
				Staff.objects.create(
					user=user,
					name=user.username,
				)
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'app/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def accountSettings(request):
	staff = request.user
	form = StaffForm(instance=staff)

	if request.method == 'POST':
		form = StaffForm(request.POST,instance=staff)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'app/account_settings.html', context)




######################### FORMS ############################

def add_students(request):
	form = StudentForm()
	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Student was created for ' + name)

			return redirect('add_student')
		

	context = {'form':form}
	return render(request, 'app/add_students.html', context)

def add_courses(request):
	form = CourseForm()
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Course '+ name + "created")

			return redirect('add_course')
		

	context = {'form':form}
	return render(request, 'app/add_course.html', context)

def add_classrooms(request):
	form = RoomForm()
	if request.method == 'POST':
		form = RoomForm(request.POST)
		if form.is_valid():
			user = form.save()
			name = form.cleaned_data.get('name')
			messages.success(request, 'Created Room no. ' + name)

			return redirect('add_classroom')
		

	context = {'form':form}
	return render(request, 'app/add_classroom.html', context)

def add_schedules(request):
	form = ScheduleForm()
	if request.method == 'POST':
		form = ScheduleForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			messages.success(request, 'Schedule Created')

			return redirect('add_schedule')
		

	context = {'form':form}
	return render(request, 'app/add_schedule.html', context)

def add_sections(request): #####NEEDS Configurations
	form = SectionForm()
	if request.method == 'POST':
		form = SectionForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			messages.success(request, 'Section Created')

			return redirect('add_section')
		

	context = {'form':form}
	return render(request, 'app/add_section.html', context)