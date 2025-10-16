
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.courses.models import Course, Lesson, Cart, Favorite, PurchasedCourse, CourseComment, LessonComment
from .serializer import CourseSerializer, CourseDetailSerializer, LessonCreateSerializer, CartSerializer, \
    CardListSerializer, FavoriteSerializer, FavoriteCourseSerializer, CourseListSerializer, PurchasedCourseSerializer, \
    PurchasedCourseListSerializer, CourseCommentSerializer, LessonCommentSerializer, CourseCommentListSerializer, \
    LessonCommentListSerializer


class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]



class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1 if instance.views else 1
        instance.save(update_fields=['views'])
        return super().get(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)



class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        # course id ni int ga aylantirish va Course obyektini olish
        try:
            course = Course.objects.get(pk=int(course_id))
        except (ValueError, Course.DoesNotExist):
            return Response({"detail": "Bunday kurs mavjud emas."}, status=400)

        # allaqachon savatchada bormi tekshirish
        if Cart.objects.filter(user=user, course=course).exists():
            return Response({"detail": "Bu kurs allaqachon savatchaga qo‘shilgan."}, status=400)

        # serializer orqali saqlash
        serializer = self.get_serializer(data={'course': course.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, course=course)
        return Response(serializer.data, status=201)



class CartListAPIView(generics.ListAPIView):
    serializer_class = CardListSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class RemoveFromCartAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs.get('pk')  # <-- URL dan olamiz

        if not course_id:
            return Response({"detail": "course ID yuborilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = Cart.objects.filter(user=user, course_id=course_id).first()
        if not cart_item:
            return Response({"detail": "Bu kurs savatchada mavjud emas."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"detail": "Kurs savatchadan olib tashlandi."}, status=status.HTTP_200_OK)


class ToggleFavoriteAPIView(generics.GenericAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)


    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        # course obyektini olish
        try:
            course = Course.objects.get(pk=int(course_id))
        except (ValueError, Course.DoesNotExist):
            return Response({"detail": "Bunday kurs mavjud emas."}, status=400)

        favorite, created = Favorite.objects.get_or_create(user=user, course=course)

        if not created:
            # allaqachon bor edi → favorite dan o‘chiramiz
            favorite.delete()
            return Response({"detail": "Kurs favorite dan olib tashlandi."}, status=200)

        return Response({"detail": "Kurs favorite ga qo‘shildi."}, status=201)


class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # faqat login qilgan foydalanuvchining favorite kurslari
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')




class PurchaseCourseAPIView(generics.CreateAPIView):
    queryset = PurchasedCourse.objects.all()
    serializer_class = PurchasedCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserPurchasedCoursesAPIView(generics.ListAPIView):
    serializer_class = PurchasedCourseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PurchasedCourse.objects.filter(user=self.request.user).select_related('course').order_by('-purchased_at')


class PurchasedCourseDeleteAPIView(generics.DestroyAPIView):
    queryset = PurchasedCourse.objects.all()
    serializer_class = PurchasedCourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Siz bu kursni o‘chira olmaysiz!")
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # ruxsatni tekshiramiz
        if instance.user != request.user:
            raise PermissionDenied("Siz bu kursni o‘chira olmaysiz!")

        course_title = instance.course.title  # kurs nomini oldindan olish
        self.perform_destroy(instance)

        return Response(
            {"message": f"'{course_title}' nomli kurs muvaffaqiyatli o‘chirildi."},
            status=status.HTTP_200_OK
        )

class CourseCommentCreateAPIView(generics.CreateAPIView):
    queryset = CourseComment.objects.all()
    serializer_class = CourseCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        course_title = serializer.instance.course.title
        return Response(
            {"message": f"‘{course_title}’ kursiga izoh muvaffaqiyatli qo‘shildi."},
            status=status.HTTP_201_CREATED
        )


class LessonCommentCreateAPIView(generics.CreateAPIView):
    queryset = LessonComment.objects.all()
    serializer_class = LessonCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        lesson_title = serializer.instance.lesson.title
        return Response(
            {"message": f"‘{lesson_title}’ darsiga izoh muvaffaqiyatli qo‘shildi."},
            status=status.HTTP_201_CREATED
        )



class CourseCommentListAPIView(generics.ListAPIView):
    serializer_class = CourseCommentListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        return CourseComment.objects.filter(course_id=course_id).order_by('-created_at')



class LessonCommentListAPIView(generics.ListAPIView):
    serializer_class = LessonCommentListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        lesson_id = self.kwargs.get('pk')
        return LessonComment.objects.filter(lesson_id=lesson_id).order_by('-created_at')


course_cooment_list = CourseCommentListAPIView.as_view()
lesson_comment_list = LessonCommentListAPIView.as_view()
course_comment_create_view = CourseCommentCreateAPIView.as_view()
lesson_comment_create_view = LessonCommentCreateAPIView.as_view()
delete_purchase_course = PurchasedCourseDeleteAPIView.as_view()
purchase_course_list = UserPurchasedCoursesAPIView.as_view()
purchase_course = PurchaseCourseAPIView.as_view()
favorite_list_view = FavoriteListAPIView.as_view()
favorite_courses = ToggleFavoriteAPIView.as_view()
card_remove = RemoveFromCartAPIView.as_view()
card_create = CartCreateAPIView.as_view()
card_list = CartListAPIView.as_view()
course_create = CourseCreateAPIView.as_view()
course_list = CourseListAPIView.as_view()
course_detail = CourseDetailAPIView.as_view()
lesson_create = LessonCreateAPIView.as_view()

