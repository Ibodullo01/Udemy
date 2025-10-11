from rest_framework import serializers
from apps.courses.models import Course, Lesson, Cart, Favorite, PurchasedCourse, LessonComment, CourseComment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'author',
            'description',
            'price',
            'rating',
            'full_description',
            'card_image',
            'thumbnail',
            'duration',
            'level',
            'category',
            'lessons_count',
        ]

        extra_kwargs = {
            'title': {'default': ''},
            'author': {'default': ''},
            'description': {'default': ''},
            'price': {'default': ''},
            'rating': {'default': ''},
            'full_description': {'default': ''},
            'thumbnail': {'default': ''},
            'duration': {'default': ''},
            'level': {'default': ''},
            'category': {'default': ''},
            'lessons_count': {'default': ''},


        }
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'course',
            'lesson_number',
            'title',
            'description',
            'video_url',
            'duration',
            'is_free',
        ]

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'author',
            'description',
            'price',
            'rating',
            'description',
            'card_image',
            'thumbnail',
            'duration',
            'level',
            'category',
            'lessons_count',
            'views',
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'author',
            'description',
            'price',
            'rating',
            'full_description',
            'card_image',
            'thumbnail',
            'duration',
            'level',
            'category',
            'lessons_count',
            'views',
            'lessons',
        ]

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'course',
            'lesson_number',
            'title',
            'description',
            'video_url',
            'duration',
            'is_free',
        ]
        extra_kwargs = {
            'course': {'default': ''},
            'lesson_number': {'default': ''},
            'title': {'default': ''},
            'description': {'default': ''},
            'video_url': {'default': ''},
            'duration': {'default': ''},
            'is_free': {'default': 'False'},
        }

    def validate(self, attrs):
        course = attrs.get('course')
        lesson_number = attrs.get('lesson_number')

        if Lesson.objects.filter(course=course, lesson_number=lesson_number).exists():
            raise serializers.ValidationError({
                "lesson_number": f"{course.title} kursida {lesson_number}-raqamli dars allaqachon mavjud."
            })

        return attrs


class CartSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_price = serializers.DecimalField(source='course.price', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'course', 'course_title', 'course_price']
        extra_kwargs = {'course': {'required': True}}

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs.get('course')

        # course string yoki int bo'lishi mumkin
        if isinstance(course, (str, int)):
            course_obj = Course.objects.filter(pk=int(course)).first()
        else:
            course_obj = course

        if not course_obj:
            raise serializers.ValidationError({"detail": "Bunday kurs mavjud emas."})

        if Cart.objects.filter(user=user, course=course_obj).exists():
            raise serializers.ValidationError({"detail": "Bu kurs allaqachon savatchaga qo‘shilgan."})

        attrs['course'] = course_obj
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        course = validated_data['course']
        return Cart.objects.create(user=user, course=course)


class CardListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'course', 'course_title', 'created_at']



class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'course']

class FavoriteCourseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='course.title', read_only=True)
    price = serializers.DecimalField(source='course.price', max_digits=8, decimal_places=2, read_only=True)
    description = serializers.CharField(source='course.description', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'course', 'title', 'price', 'description', 'created_at']



class PurchasedCourseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_price = serializers.DecimalField(source='course.price', max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = PurchasedCourse
        fields = ['id', 'user', 'course', 'course_title', 'course_price', 'purchased_at']
        read_only_fields = ['id', 'user', 'purchased_at']

    def create(self, validated_data):
        user = self.context['request'].user
        course = validated_data['course']

        # oldin sotib olingan bo‘lsa, xatolik qaytaramiz
        if PurchasedCourse.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Siz bu kursni allaqachon sotib olgansiz!")

        purchase = PurchasedCourse.objects.create(user=user, course=course)
        return purchase

class PurchasedCourseListSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_author = serializers.CharField(source='course.author', read_only=True)
    course_price = serializers.DecimalField(source='course.price', max_digits=8, decimal_places=2, read_only=True)
    course_rating = serializers.FloatField(source='course.rating', read_only=True)

    class Meta:
        model = PurchasedCourse
        fields = ['id', 'course', 'course_title', 'course_author', 'course_price', 'course_rating', 'purchased_at']



class CourseCommentSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.fullname', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseComment
        fields = ['id', 'course', 'course_title', 'user_fullname', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_fullname', 'course_title']

    def create(self, validated_data):
        user = self.context['request'].user
        course = validated_data['course']
        text = validated_data['text']
        comment = CourseComment.objects.create(user=user, course=course, text=text)
        return comment


class LessonCommentSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.fullname', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonComment
        fields = ['id', 'lesson', 'lesson_title', 'user_fullname', 'text', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_fullname', 'lesson_title']

    def create(self, validated_data):
        user = self.context['request'].user
        lesson = validated_data['lesson']
        text = validated_data['text']
        comment = LessonComment.objects.create(user=user, lesson=lesson, text=text)
        return comment


class CourseCommentListSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.fullname', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseComment
        fields = ['id', 'text', 'user_fullname', 'course_title', 'created_at']


class LessonCommentListSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.fullname', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonComment
        fields = ['id', 'text', 'user_fullname', 'lesson_title', 'created_at']